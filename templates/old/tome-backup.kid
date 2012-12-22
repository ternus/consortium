<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Carbuncle Archives</title>
</head>
<body>

  <div class="main_content">
    <div style="float:right; width: 12em; padding: 5px; border-left: 2px solid #aaa">
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
      <li> North: <span py:replace="XML(neighbors.north)">foo</span> </li>
      <li> Northeast: <span py:replace="XML(neighbors.northeast)">foo</span> </li>
      <li> Southeast: <span py:replace="XML(neighbors.southeast)">foo</span> </li>
      <li> South: <span py:replace="XML(neighbors.south)">foo</span> </li>
      <li> Southwest: <span py:replace="XML(neighbors.southwest)">foo</span> </li>
      <li> Northwest: <span py:replace="XML(neighbors.northwest)">foo</span> </li>
    </ul>
  </div>
  <div class="html_body" py:replace="XML(cardcatalogs)"></div>

</body>
</html>

