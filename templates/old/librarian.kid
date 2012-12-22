<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Grant Access to Tome</title>
</head>

<body>
    <div>
        <h1>Grant Access to Tome</h1>
	<p>
	  This form allows a librarian or researcher to grant another
	  person access to a tome in the Archives. With this access,
	  the target will gain a shortcut in their sidebar to go
	  directly to the node in question, and will be able to skip
	  over other nodes in the archives to get there. This is
	  intended to save the other person time and Inspiration.
	</p>
        <form action="shortcut" method="POST">
	  Character being granted access: <input type="text" name="targetname" rows="1" cols="40"/><br/>
	  Tome to grant access to: <textarea name="targettome" py:content="title"/><br/>
          <input type="submit" name="submit" value="Grant Access to Tome"/>
        </form>
    </div>
</body>
</html>
