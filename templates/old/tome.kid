<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>The Market</title>
</head>
<body>
  <div class="main_content">
    <div style="float:right; width: 12em; padding: 5px; border-left: 1px solid #aaa">
      <span py:replace="character.name">Random Character</span> has a research stat of <i><span py:replace="character.research">N</span></i> and a current Research Inspiration of <i><span py:replace="character.inspiration">M</span></i>.<p/><p><a href="/spend">Spend Raw Inspiration for more Research Inspiration here.</a></p>
      You are viewing <b><span py:replace="tome.title">Tome Title Goes Here</span></b>
      at hex (<span py:replace="tome.hex">XXYY</span>)
      <br/>
      Shortcuts:<br/>
      <div class="html_body" py:replace="XML(shortcuts)">Shortcuts go here.</div>
    </div>
  </div>
  <div class="html_body" py:replace="XML(text)">Page text goes here.</div>
  <div class="main_content">
    <ul>
      <span py:replace="XML(neighborwad)">Foo.</span>
    </ul>
  </div>
  <div class="html_body" py:replace="XML(cardcatalogs)"></div>
  <div id="floatclear" />
  
</body>
</html>

