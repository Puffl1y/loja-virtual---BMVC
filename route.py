from bottle import Bottle, run, request, response, static_file, redirect, HTTPResponse
from app.controllers.application import Application

app = Bottle()
ctl = Application()


def require_authentication():
    if not ctl.is_authenticated():
        raise HTTPResponse(status=401, body='Acesso negado. Faça login em /portal.\n',
                            headers={"Content-Type": "text/plain; charset=UTF-8"})


def product_payload():
    data = request.json
    if not isinstance(data, dict):
        raise ValueError("Envie um objeto JSON no corpo da requisição.")
    required = ("nome", "categoria", "preco", "tamanho", "cor")
    missing = [field for field in required if field not in data]
    if missing:
        raise ValueError("Campos obrigatórios ausentes: " + ", ".join(missing))
    for field in ("nome", "categoria", "tamanho", "cor"):
        if not str(data[field]).strip():
            raise ValueError(f"O campo '{field}' não pode ficar vazio.")
    try:
        price = float(data["preco"])
        if price < 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("O preço deve ser um número maior ou igual a zero.")
    return {**data, "preco": price}


@app.get('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.get('/')
def home():
    redirect('/portal')

@app.get('/helper')
def helper():
    return ctl.render('helper')

@app.get('/portal')
def portal():
    if ctl.is_authenticated():
        redirect('/banco')
    return ctl.portal()

@app.post('/portal')
def action_portal():
    username = request.forms.get('username', '').strip()
    password = request.forms.get('password', '')
    session_id = ctl.authenticate_user(username, password)
    if not session_id:
        response.status = 401
        return ctl.portal(error='Usuário ou senha inválidos.')
    # secure=False permite testar com HTTP em localhost. Em HTTPS, altere para True.
    response.set_cookie('session_id', session_id, httponly=True,
                        secure=False, samesite='Lax', max_age=3600, path='/')
    redirect('/banco')

@app.get('/banco')
def banco():
    return ctl.render('banco')

@app.post('/logout')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id', path='/')
    redirect('/portal')

# API de gerenciamento: as três operações são realizadas via CURL.
@app.post('/api/produtos')
def create_product():
    require_authentication()
    try:
        product = ctl.models.create_product(product_payload())
        response.status = 201
        response.content_type = 'application/json; charset=UTF-8'
        return {"mensagem": "Produto cadastrado com sucesso.", "produto": product.to_dict()}
    except (ValueError, TypeError, KeyError) as error:
        raise HTTPResponse(status=400, body=str(error),
                           headers={"Content-Type": "text/plain; charset=UTF-8"})

@app.put('/api/produtos/<product_id:int>')
def update_product(product_id):
    require_authentication()
    try:
        product = ctl.models.update_product(product_id, product_payload())
        if not product:
            raise HTTPResponse(status=404, body='Produto não encontrado.\n')
        response.content_type = 'application/json; charset=UTF-8'
        return {"mensagem": "Produto atualizado com sucesso.", "produto": product.to_dict()}
    except (ValueError, TypeError, KeyError) as error:
        raise HTTPResponse(status=400, body=str(error),
                           headers={"Content-Type": "text/plain; charset=UTF-8"})

@app.delete('/api/produtos/<product_id:int>')
def delete_product(product_id):
    require_authentication()
    if not ctl.models.delete_product(product_id):
        raise HTTPResponse(status=404, body='Produto não encontrado.\n')
    response.content_type = 'application/json; charset=UTF-8'
    return {"mensagem": f"Produto {product_id} excluído com sucesso."}

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True, reloader=False)
