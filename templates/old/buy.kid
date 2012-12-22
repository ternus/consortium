<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Item Purchased!</title>
</head>

<body>
    <div>
        <h1></h1>
        <p>Congratulations! You bought <span py:replace="item.name">the item</span>!<br/>
	  Your item number is <span py:replace="item.itemcardno">999</span> -- fetch it from the box.<br/>
	  <span py:replace="XML(goback)"></span></p>
    </div>
</body>
</html>
