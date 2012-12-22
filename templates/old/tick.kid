<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Advance Time!</title>
</head>

<body>
    <div>
        <h1>Move Time Forward</h1>
	Time was last advanced on: <span py:replace="date">now</span>.
        <form action="advancetime" method="POST">
          <input type="submit" name="submit" value="GO"/>
        </form>
    </div>
</body>
</html>
