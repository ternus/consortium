<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Rumor</title>
</head>

<body>
    <div>
        <h1></h1>
        <p>After talking at length
	  with <span py:replace="node.name">some guy</span>, you learn
	  some information
	  about <span py:replace="rumor.subject">something</span>.
	  <blockquote>
	    <span py:replace="rumor.text">Secrets and lies!</span>
	  </blockquote>
	  <br/>
	  <span py:replace="XML(goback)"></span>  <span py:replace="XML(squelch)"></span></p>
    </div>
</body>
</html>
