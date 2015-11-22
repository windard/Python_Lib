##Install Sublime Text In Linux

####Install via the Package Manager(apt-get):

For Sublime-Text-2     
```
sudo add-apt-repository ppa:webupd8team/sublime-text-2
sudo apt-get update
sudo apt-get install sublime-text
```

For Sublime-Text-3
```
sudo add-apt-repository ppa:webupd8team/sublime-text-3
sudo apt-get update
sudo apt-get install sublime-text-installer
```

####Install Manually via Terminal:
Download from the Sublime Site:   

32-bit:     
```
wget http://c758482.r82.cf2.rackcdn.com/Sublime\ Text\ 2.0.2.tar.bz2
tar vxjf Sublime\ Text\ 2.0.2.tar.bz2
cd Sublime\ Text\ 2
./sublime_text
```

64-bit:       
```
wget http://c758482.r82.cf2.rackcdn.com/Sublime\ Text\ 2.0.2\ x64.tar.bz2
tar vxjf Sublime\ Text\ 2.0.2\ x64.tar.bz2
cd Sublime\ Text\ 2
./sublime_text
```

For Both:         
```
sudo mv Sublime\ Text\ 2 /opt/
sudo ln -s /opt/Sublime\ Text\ 2/sublime_text /usr/bin/subl
```

OK,now you can use `subl` in terminal to open your  sublime .    
