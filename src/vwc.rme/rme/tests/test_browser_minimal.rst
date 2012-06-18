kotti_rme browser tests
============================

Setup and Login
---------------

  >>> from kotti import tests
  >>> tools = tests.setUpFunctional(
  ...     **{'kotti.configurators': 'kotti_rme.kotti_configure'})
  >>> browser = tools['Browser']()
  >>> ctrl = browser.getControl

  >>> browser.open(tests.BASE_URL + '/@@login')
  >>> "Log in" in browser.contents
  True
  >>> ctrl("Username or email").value = "admin"
  >>> ctrl("Password").value = "secret"
  >>> ctrl(name="submit").click()
  >>> "Welcome, Administrator" in browser.contents
  True
