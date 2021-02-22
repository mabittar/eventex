# Django
---

Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Thanks for checking it out.

All documentation is in the "docs" directory and online at https://docs.djangoproject.com/en/stable/. If you're just getting started, here's how we recommend you read the docs:

## WebApp

<table>
<tr>
<td>
  A webapp using DJANGO for a great event in RJ.
</td>
</tr>
</table>

## Ready is when it's online!
[Eventex Website](https://eventex-mmb.herokuapp.com/) - check the website online!!!


## Como desenvolver?

  1. clone o repositório
  2. crie o venv com Python 3.6 ou superior
  3. ative o venv
  4. instale as dependências utilizando `pip install -r requirements.txt`
  5. configure a instância com .env utilizando `cp contrib/.env-sample .env` esse comando vai copiar o arquivo que está na pasta contrib para a raíz do seu diretório. É necessário editá-lo com as suas configurações.
  6. execute os testes com `python manage.py test`

  ## Como fazer o Deploy?
  1. crie uma instância no heroku utilizando `heroku create meu_projeto`
  2. envie suas configurações para o heroku com `heroku config:push`
  3. defina uma SECRET_KEY com `heroku config:set SECRET_KEY=sua_senha`
  4. defina DEBUG=False `heroku config:set DEBUG=False`
  5. configure o serviço de e-mail - esse passo depende muito do serviço a ser utilizado consulte SendGrid para maiores detalhes
  6. envie o código para o heroku utilizando `git push heroku master --force`