<?php 	
// $file2 = fopen("测试.txt", 'w');
// fwrite($file2,"这是测试文件");
// fclose($file2);
$filename=iconv('utf-8','gb2312',"测试文档.txt");
$file3 = fopen($filename,'r');
$content = fread($file3,filesize($filename));
echo $content;
fclose($file3);
 ?>