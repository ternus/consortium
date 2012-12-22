<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<script language="javascript" type="text/javascript" >
<!-- hide

function jumpto(x){

if (document.sform.jumpmenu.value != "null") {
document.location.href = x
}
}

// end hide -->
</script>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>GM CONTROL PANEL</title>
</head>
<body>
  <div class="main_content">
    <h1>GM CONTROL PANEL</h1>
<form name="sform">	  
    <p><a href="/tick">Advance Time</a></p>
    <p><a href="/allmap">View Full Map</a></p>
    <p><a href="/manualpop">Manually Populate Rumors</a></p>
    <p>View Map For: <select name="jumpmenu" onchange="if (this.selectedIndex > 0) location.href='/gmmap/'+this[this.selectedIndex].value;">
<option>Select Character</option>
<span py:replace="XML(charlist)">****ERROR****</span></select></p>
    <p>Jump To: <select name="jumpmenu" onchange="if (this.selectedIndex > 0) location.href='/'+this[this.selectedIndex].value;">
<option>Select Node</option>
<span py:replace="XML(nodelist)">****ERROR****</span></select></p></form>

<form action="kill" method="POST">
    <p>Kill: 
<select name="char">
<option>Select Character</option>
<span py:replace="XML(charlist)">****ERROR****</span>
</select>

<select name="hex">
<option>Select Node</option>
<span py:replace="XML(nodelist)">****ERROR****</span>
</select>

<select name="disguised"><option>Disguised?</option><option value='1'>Yes</option><option value='0'>No</option></select>
<input type="submit" name="submit" value="KILL"/></p>

</form>
    
  </div>
  <div id="floatclear" />
  
</body>
</html>

