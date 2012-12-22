<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Transfer Money</title>
</head>

<body>
    <div>
        <h1>Transfer Money</h1>
        <p>This form allows you to transfer money to another character.
	  Your current Wealth is <b><span py:replace="char.wealth">a lot of</span> deben</b>.
         
	<a href="javascript: history.go(-1)">Cancel</a>.</p>

	
        <form action="transfercommit" method="POST">
	  Transfer <input type="text" name="amount" value="0" size="2" onFocus="this.value=''"/> deben to 
	  <!-- <input type="text" name="character" content="Character Name" size="20" onFocus="this.value=''"/> -->
	  <span py:replace="XML(charlist)">****ERROR****</span>
          <input type="submit" name="submit" value="Transfer"/>
        </form>
    </div>
</body>
</html>
