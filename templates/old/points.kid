<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
    <title>Check or Modify Points</title>
</head>

<body>
    <div>
        <h1>Check or Modify Points</h1>
        <p><b>You have <span py:replace="char.points">ONE MILLION</span> Market points.</b></p> 
	<p>Your market stat is <span py:replace="char.marketstat">1</span>.</p>

        <p><b>You have <span py:replace="char.wealth">ONE MILLION</span> deben.</b></p> 
	<p>Your Income stat is <span py:replace="char.incomestat">1</span>.</p>

	<a href="javascript: history.go(-1)">Cancel</a>.<p/>

	<hr/>
	
	<p>The form below will allow you to modify these numbers.  Only
	do this if you know you can.</p>
	<p><b>Note</b>:  Use <a href="/transfer">this form</a> to transfer money.</p>

	<p>Enter the amount to add (negative to remove) in the boxes.
	Enter the source of these points in the "Reason" box.</p>

        <form action="spendcommit" method="POST">
	  Modify Market Points: <input type="text" name="market" value="0" size="2"/><br/>
	  Modify Money: <input type="text" name="money" value="0" size="2"/><br/>
	  Reason: <input type="text" name="reason"/><br/> 
          <input type="submit" name="submit" value="Apply"/>
        </form>
	
	<hr/>
	
	<p py:if="not char.hasdisguise">If you know you can, you can
	click <a href="/setdisguise">here</a> to give yourself the
	Disguise ability.</p>
	<p py:if="char.hasdisguise">If you know you must, you can
	click <a href="/setdisguise">here</a> to remove the
	Disguise ability.</p>
	
    </div>
</body>
</html>
