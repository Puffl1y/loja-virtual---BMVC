<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OASIS | Portal</title><link rel="stylesheet" href="/static/css/aura.css">
</head>
<body class="login-page">
  <main class="login-card">
    <a class="brand" href="/portal">OASIS<span>.</span></a>
    <p class="eyebrow">GESTÃO DA LOJA</p>
    <h1>Bem-vinda de volta!</h1>
    <p class="muted">Entre para acessar o banco de produtos da OASIS.</p>
    % if error:
      <div class="alert">{{error}}</div>
    % end
    <form action="/portal" method="post" class="login-form">
      <label for="username">Usuário</label>
      <input id="username" name="username" type="text" placeholder="Seu usuário" required autocomplete="username">
      <label for="password">Senha</label>
      <input id="password" name="password" type="password" placeholder="Sua senha" required autocomplete="current-password">
      <button class="button primary full" type="submit">Entrar no portal <span>→</span></button>
    </form>
    <p class="hint">Acesso de demonstração: <strong>admin</strong> / <strong>aura123</strong></p>
  </main>
  <div class="login-decoration decoration-one"></div><div class="login-decoration decoration-two"></div>
</body></html>
