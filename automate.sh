#/bin/bash

if [[ -r /etc/os-release ]]; then
	debian_codename=$(cat /etc/os-release  | grep VERSION_CODENAME | awk -F "=" '{ print $2 }')
	
	if [[ ${#debian_codename} -gt 0 ]]; then
	
		echo "codename: "$debian_codename
		F_=0
		for file in $(find /etc/apt/ -type f -name "*.list"); do 
			while read p; do
				cleaned_=$(echo "$p" | grep -v ^# | grep -v ^$ | grep "deb-src")
				if [[ $cleaned_ == *"debian buster main"* ]]; then
					F_=1
					F_file=$file
				fi
			done < "$file"
		done
		echo "F: "$F_
		if [[ $F_ -eq 0 ]]; then
			F_b=0
			for file in $(find /etc/apt/ -type f -name "*.list"); do 
				while read p; do
					cleaned_=$(echo "$p" | grep -v ^# | grep -v ^$ | grep -v "deb-src")
					if [[ $cleaned_ == *"debian buster main"* ]]; then
						F_b=cleaned_
					fi
				done < "$file"
			done
			new_line = $(echo $cleaned_ | sed -r 's/deb /deb-src /g')
			echo $new_line >> /etc/apt/sources.list
			apt update
		else
			apt-get update
			apt-get install -y wget openssl devscripts build-essential libssl-dev
			apt-get source squid -y
			if [[ ! -r squid-4.6/debian/rules.patched ]]; then
				wget -q  https://raw.githubusercontent.com/Whatsyourlanguage-World/squid4-ssl/master/8ce644cfad297651f8848895cad28dc3d405b888.patch -O - | patch -p2 squid-4.6/debian/rules
				echo 1 > squid-4.6/debian/rules.patched
			fi
			cd squid-4.6
			debuild -us -uc
		fi
	
	fi

fi
