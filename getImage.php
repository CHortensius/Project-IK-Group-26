<?php
  $link = mysql_connect("localhost", "root", "");
  mysql_select_db("accounts.db");
  $sql = "SELECT * FROM pics";
  $result = mysql_query("$sql");
  $row = mysql_fetch_assoc($result);
  mysql_close($link);

  header("Content-type: image/jpeg");
  echo $row['url'];
?>