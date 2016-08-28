#!/usr/bin/php
<?php

 include '../domains/ithld.linuxpl.info/public_html/geck/conf.php';
 
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TU WPISAĆ ZAKONCZONY MIESIĄC
$query='SELECT * FROM `results` WHERE year( date ) =2013 AND month( date ) ='.date("m", strtotime("-1 month"));
 
 $wynik=mysql_query($query);
 $ilosc_wynikow=mysql_num_rows($wynik);
 for($i=0;$i<$ilosc_wynikow;$i++){
 	$baza=mysql_fetch_assoc($wynik);
 	$baza_ar=mysql_fetch_assoc(mysql_query("select count(*) as ile from `archive` where `key`='{$baza['key']}' and `date`='{$baza['date']}'"));
 	
	if($baza_ar['ile']==0){ 	
		$sql="insert into `archive` set `key`='{$baza['key']}', `pos`='{$baza['pos']}', `date`='{$baza['date']}'";
		$temp=mysql_query("insert into `archive` set `key`='{$baza['key']}', `pos`='{$baza['pos']}', `date`='{$baza['date']}'");
		echo $temp."-".$sql."\n";
		echo mysql_error();		
	}
 }

 
  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TU WPISAĆ ZAKONCZONY MIESIĄC
$query='DELETE FROM `results` WHERE year( date ) =2013 AND month( date ) =03';
$sql=mysql_query($query) or die(mysql_error());  

?>
