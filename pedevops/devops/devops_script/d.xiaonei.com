;
; BIND reverse data file for local loopback interface
;
$TTL	300
@	IN	SOA	d.xiaonei.com. root.d.xiaonei.com. (
		     2016071202		; Serial
			 604801		; Refresh
			    900		; Retry
			2419200		; Expire
			     60 )	; Negative Cache TTL
;
@	IN	NS	ns1.d.xiaonei.com.
@	IN	NS	ns2.d.xiaonei.com.
@	IN	NS	ns3.d.xiaonei.com.
@	IN	NS	ns4.d.xiaonei.com.
@	IN	NS	ns5.d.xiaonei.com.
@	IN	NS	ns6.d.xiaonei.com.

ns1	IN	A	10.4.24.38
ns2	IN	A	10.4.24.136
ns3	IN	A	10.4.30.135

; yum mirror & private repo
$TTL	60
mirrors	IN	A	10.4.1.45
psa	IN	A	10.4.16.33
yum	IN	A	10.4.1.45
bj.yum	IN	A	10.4.1.45

; SOM
ntm	IN	A	10.4.26.112
som		IN	A	10.4.1.21

