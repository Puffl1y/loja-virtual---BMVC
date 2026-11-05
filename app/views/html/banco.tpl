<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OASIS | Banco de produtos</title><link rel="stylesheet" href="/static/css/aura.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/banco">OASIS<span>.</span></a>
    <div class="top-actions"><span class="user-chip">Olá, {{current_user.username}}</span>
      <form action="/logout" method="post"><button class="button light" type="submit">Sair</button></form>
    </div>
  </header>
  <main class="container">
    <section class="welcome">
      <div><p class="eyebrow">PAINEL ADMINISTRATIVO</p><h1>Banco de produtos</h1>
        <p class="muted">Consulte os itens cadastrados na loja OASIS.</p></div>
      <div class="stat-card"><span>PRODUTOS CADASTRADOS</span><strong>{{len(produtos)}}</strong></div>
    </section>
    <section class="section-heading"><div><p class="eyebrow">INVENTÁRIO</p><h2>Todos os produtos</h2></div>
      <span class="count-pill">{{len(produtos)}} itens</span></section>
    % if produtos:
      <div class="product-grid">
      % for produto in produtos:
        <article class="product-card">
          <div class="product-art"><span>{{produto.categoria}}</span><div class="hanger">✳</div></div>
          <div class="product-info"><div class="product-title"><h3>{{produto.nome}}</h3><strong>R$ {{'%.2f' % produto.preco}}</strong></div>
            <p>{{produto.categoria}} · Tamanho {{produto.tamanho}}</p><div class="product-footer"><span>Cor: {{produto.cor}}</span><small>ID #{{produto.id}}</small></div>
          </div>
        </article>
      % end
      </div>
    % else:
      <div class="empty-state"><div>✳</div><h3>Nenhum produto cadastrado</h3><p>Use o CURL no terminal para cadastrar o primeiro produto.</p></div>
    % end
  </main>
  <footer>OASIS — moda que mostra quem você é.</footer>
</body></html>
