#!/bin/bash

VERSION='0.8.1'
UPLOAD_ITERATOR='1'

DISTROS='
hardy
intrepid
jaunty
karmic
lucid
maverick
natty
oneiric
precise
'

DEB_HELPER_6='hardy
intrepid'

DEB_HELPER_7='jaunty
karmic
lucid'

DEB_HELPER_8='maverick
natty
oneiric
precise'

DATE=`date --rfc-2822`

FIRST_DISTRO=$(echo $DISTROS | cut -d" " -f1)

# Update the About glade file
sed -i "s/<property name=\"version\">[0-9]*.[0-9]*.[0-9]*<\/property>/<property name=\"version\">$VERSION<\/property>/g" ../ui/About.glade

# Update Makefile
sed -i "s/VERSION ?= [0-9]*.[0-9]*.[0-9]*/VERSION ?= $VERSION/g" ../Makefile

# Update spec file
sed -i "s/Version:[ ]*[0-9]*.[0-9]*.[0-9]*/Version:       $VERSION/g" ../sopcast-player.spec

# Update changelog timestamp
sed -i "s/ -- Jason Scheunemann <jason.scheunemann@yahoo.com>  .*/ -- Jason Scheunemann <jason.scheunemann@yahoo.com>  $DATE/g" ./changelog

# Update changelog version 
sed -i "0,/([0-9]*.[0-9]*.[0-9]*~/s//($VERSION~/" changelog


if [[ -n `cat 'changelog' | grep -E '~ppa*~(hardy|intrepid|jaunty|karmic|lucid|maverick|natty|oneiric|precise)[0-9]*'` ]]
then
	for REPLACEMENT_DISTRO in ${DISTROS};
	do	
		sed -i "0,/~[a-z]*[0-9]*) [a-z]*;/s//~$REPLACEMENT_DISTRO$UPLOAD_ITERATOR) $REPLACEMENT_DISTRO;/" changelog
		
		for DISTRO in ${DEB_HELPER_6};
		do		
			if [ ${REPLACEMENT_DISTRO} == ${DISTRO} ]
			then
				echo 6 > compat
			fi
		done

		for DISTRO in ${DEB_HELPER_7};
		do		
			if [ ${REPLACEMENT_DISTRO} == ${DISTRO} ]
			then
				echo 7 > compat
			fi
		done

		for DISTRO in ${DEB_HELPER_8};
		do		
			if [ ${REPLACEMENT_DISTRO} == ${DISTRO} ]
			then
				echo 8 > compat
			fi
		done
			
		debuild -S -sa
		wait
		dput my-ppa '../../'`cat 'changelog' | awk 'NR < 2' | sed 's/ (/_/g' | sed 's/).*/_source.changes/g'`
		
	done
	
	echo 'Cleaning up...'
	rm -rf ../../*.dsc ../../*.changes ../../*.tar.gz ../../*.build ../../*.upload
else
	echo 'Error in the format of the chanelog file!'
	echo 'Package must be in the form of <pacakge name> (<version>~ppa<[0-9]*>~<release><[0-9]*>).'
fi


