# Introduction #

This page explanis how to install Pyjamas and the pyjamas desktop on Ubuntu 9.10.

See this page instead if you have a few hours to spare building the XUL lib or need/want background information on pyjamas dependencies:

http://code.google.com/p/pyjamas/wiki/PyjamasUbuntu

# Checkout Pyjamas #

For illustration purposes, create a new directory in your home directory called tools. (Feel free to install pyjamas anywhere, but the rest of this guide will refer to ~\tools).

Checkout pyjamas with svn into your ~/tools directory:

```
$ svn co https://pyjamas.svn.sourceforge.net/svnroot/pyjamas/trunk pyjamas
```

This should create a directory ~/tools/pyjamas/ containing the current development source code.

# Install Pyjamas #

Now "install pyjamas" with the bootstrap command.
```
$ cd pyjamas

$ python bootstrap.py 
```


This creates a directory bin/ which contains two wrapper programs:

```
pyjamas$ ls bin/
pyjampiler  pyjsbuild  pyjscompile
```

The pyjsbuild program builds a web application.

It also creates the file pyjd/init.py for pyjamas-desktop integration.

# Setup Pyjamas on your PATH #
The programs in bin/ can be executed from anywhere and will locate the pyjamas program files automatically. You can add this directory to your PATH variable, for example:

```
pyjamas$ export PATH=~/tools/pyjamas/bin:$PATH
```

The rest of this guide assumes that you have added ~/tools/pyjamas/bin to your path.

# Testing Pyjamas #

A first test can be done now:

```
$ pwd
~/tools/pyjamas

$ cd examples/helloworld/
$ pyjsbuild Hello.py
```

This generates a directory output/ which contains a Hello.html file and a lot of other files and directories:

```
pyjamas/examples/helloworld$ ls output/
bootstrap.js                   disclosurePanelOpen.png   Hello.ie6.cache.html
Hello.opera.cache.html         tree_closed.gif           bootstrap_progress.js
gchart.gif                     Hello.mozilla.cache.html  Hello.safari.cache.html
tree_open.gif                  disclosurePanelClosed.png Hello.css
Hello.nocache.html             history.html              tree_white.gif
disclosurePanelClosed_rtl.png  Hello.html                Hello.oldmoz.cache.html
lib/
```

Now point your browser to [file:///.../pyjamas/examples/helloworld/output/Hello.html](file:///.../pyjamas/examples/helloworld/output/Hello.html) to see if this works:

```
$ pwd
~/tools/pyjamas/examples/helloworld/

$ firefox output/Hello.html
```

# Setting Up Pyjamas-Desktop #

To run pyjamas-desktop, we have to set the python path to the pyjamas library, so pyjd can find it:

```
pyjamas$ export PYTHONPATH=~/tools/pyjamas/library:~/tools/pyjamas
```

## Installing Hulahop ##

Pyjamas desktop depends on Hulahop.

"HulaHop is Gecko 1.9 (Firefox 3.0 core) web browser as a simple embeddable control with Python DOM access. It is a PyGTK Widget." (Google search results)

Normally you can just grap hulahop as follows:

```
$ sudo apt-get install python-hulahop
```

However there are issues so you have to build HulaHop as follows:

```
$ mkdir ~/build-hulahop
$ cd ~/build-hulahop
$ sudo apt-get build-dep hulahop
$ sudo apt-get -b source hulahop
$ sudo dpkg -i python-hulahop_0.4.9-1ubuntu2_{your architecture}.deb 
```

## Installing xpcom ##
Ensure you have XUL runner installed:

```
$ apt-get install xulrunner-1.9.1
```

(I am not sure about the above step.)

Download the tar file listed below for xpcom, untar it, and copy the xpcom directory into ~/tools/pyjamas/library.

http://pyjamas-dev.googlegroups.com/web/xpcom-ubuntu-9.10.tar.gz