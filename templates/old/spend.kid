<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Spend Inspiration</title>
</head>

<body>
    <div>
        <h1>Spend Raw Inspiration</h1>
        <p>This form allows you to spend raw inspiration to gain more
        Research-typed Inspiration points. We provide your characters'
        Research stat below, but we allow you to modify the number
        shown in case you have come into possession of items or
        equipment which alter your Research stat. Please enter your
        Research Stat below and click the button to spend a point of
        Inspiration. To cancel, hit your Back button or go back to
        the <a href="/">Starting Tome</a>.</p>
	
        <form action="spendcommit" method="POST">
	  <textarea name="research" py:content="char.research" rows="1" cols="3"/>
          <input type="submit" name="submit" value="Spend 1 point Raw Inspiration"/>
        </form>
    </div>
</body>
</html>
