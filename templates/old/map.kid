<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>The Market</title>
</head>
<body>
  <div class="main_content">
    <h1>Your Map</h1>
    <i>Remember that this map is not in game!  Do not share it with anyone.</i><br/>
    <!-- <a href="javascript: history.go(-1)">Go back</a>.<p/>-->
	 <a href="/">Return to Bazaar</a>
	 <span py:if="len(character.nodes) > 0 or character.marketstat > 0" py:replace="XML(goback)">error</span>

    <span py:replace="XML(map)">Image </span>
  </div>
  <div id="floatclear" />
  
</body>
</html>

