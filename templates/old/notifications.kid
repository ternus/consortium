<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>The Market</title>
</head>
<body>
  <div class="main_content">
    <h1>Notifications</h1>
    <p><a href="/">Return to the Bazaar.</a> <span  py:if="character.marketstat > 0" py:replace="XML(goback)">foo</span></p>
    <ul>
      <span py:replace="XML(notifications)">Foo.</span>
    </ul>
  </div>
<!--  <div class="html_body" py:replace="XML(cardcatalogs)"></div> -->
  <div id="floatclear" />
  
</body>
</html>

