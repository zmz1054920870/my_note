### Zeal离线文档的使用

```html
1.手动下载我们要的文档
2.进入C:\Users\zmz\AppData\Local\Zeal\Zeal\docsets中没有的话自己创建docsets这个文件夹，把我下载好的包，放进去解压，然后继续再解压


```

```sql
#!/usr/local/bin/tclsh8.6
#LOAD LIBRARIES AND MODULES
set library tdbc::odbc
set version 1.1.1
if [catch {package require $library $version} message] { error "Failed to load $library - $message" }
if [catch {::tcl::tm::path add modules} ] { error "Failed to find modules directory" }
if [catch {package require tpchcommon} ] { error "Failed to load tpch common functions" } else { namespace import tpchcommon::* }
proc UpdateStatistics { odbc db azure } {
puts "UPDATING SCHEMA STATISTICS"
if {!$azure} {
$odbc evaldirect "CREATE OR ALTER PROCEDURE dbo.sp_updstats
with execute as 'dbo'
as
exec sp_updatestats
"
$odbc evaldirect "EXEC dbo.sp_updstats"
} else {
set sql(1) "USE $db"
set sql(2) "EXEC sp_updatestats"
for { set i 1 } { $i <= 2 } { incr i } {
$odbc evaldirect $sql($i)
                }
        }
return
}

proc CreateDatabase { odbc db azure } {
set table_count 0
puts "CHECKING IF DATABASE $db EXISTS"
set rows [ odbc allrows "IF DB_ID('$db') is not null SELECT 1 AS res ELSE SELECT 0 AS res" ]
set db_exists [ lindex {*}$rows 1 ]
if { $db_exists } {
if {!$azure} {$odbc evaldirect "use $db"}
set rows [ odbc allrows "select COUNT(*) from sys.tables" ]
set table_count [ lindex {*}$rows 1 ]
if { $table_count == 0 } {
puts "Empty database $db exists"
puts "Using existing empty Database $db for Schema build"
        } else {
puts "Database with tables $db exists"
error "Database $db exists but is not empty, specify a new or empty database name"
        }
} else {
puts "CREATING DATABASE $db"
$odbc evaldirect "create database $db"
        }
}

proc CreateTables { odbc colstore } {
puts "CREATING TPCH TABLES"
if { $colstore } {
set sql(1) "create table dbo.customer (c_custkey bigint not null, c_mktsegment char(10) null, c_nationkey int null, c_name varchar(25) null, c_address varchar(40) null, c_phone char(15) null, c_acctbal money null, c_comment varchar(118) null, index cust_cs clustered columnstore)" 
set sql(2) "create table dbo.lineitem (l_shipdate date null, l_orderkey bigint not null, l_discount money not null, l_extendedprice money not null, l_suppkey int not null, l_quantity bigint not null, l_returnflag char(1) null, l_partkey bigint not null, l_linestatus char(1) null, l_tax money not null, l_commitdate date null, l_receiptdate date null, l_shipmode char(10) null, l_linenumber bigint not null, l_shipinstruct char(25) null, l_comment varchar(44) null, index lineit_cs clustered columnstore)" 
set sql(3) "create table dbo.nation(n_nationkey int not null, n_name char(25) null, n_regionkey int null, n_comment varchar(152) null, index nation_cs clustered columnstore)" 
set sql(4) "create table dbo.part( p_partkey bigint not null, p_type varchar(25) null, p_size int null, p_brand char(10) null, p_name varchar(55) null, p_container char(10) null, p_mfgr char(25) null, p_retailprice money null, p_comment varchar(23) null, index part_cs clustered columnstore)" 
set sql(5) "create table dbo.partsupp( ps_partkey bigint not null, ps_suppkey int not null, ps_supplycost money not null, ps_availqty int null, ps_comment varchar(199) null, index psupp_cs clustered columnstore)" 
set sql(6) "create table dbo.region(r_regionkey int not null, r_name char(25) null, r_comment varchar(152) null, index region_cs clustered columnstore)"
set sql(7) "create table dbo.supplier( s_suppkey int not null, s_nationkey int null, s_comment varchar(102) null, s_name char(25) null, s_address varchar(40) null, s_phone char(15) null, s_acctbal money null, index suppl_cs clustered columnstore)" 
set sql(8) "create table dbo.orders( o_orderdate date null, o_orderkey bigint not null, o_custkey bigint not null, o_orderpriority char(15) null, o_shippriority int null, o_clerk char(15) null, o_orderstatus char(1) null, o_totalprice money null, o_comment varchar(79) null, index ord_cs clustered columnstore)"
	} else {
set sql(1) "create table dbo.customer (c_custkey bigint not null, c_mktsegment char(10) null, c_nationkey int null, c_name varchar(25) null, c_address varchar(40) null, c_phone char(15) null, c_acctbal money null, c_comment varchar(118) null)" 
set sql(2) "create table dbo.lineitem (l_shipdate date null, l_orderkey bigint not null, l_discount money not null, l_extendedprice money not null, l_suppkey int not null, l_quantity bigint not null, l_returnflag char(1) null, l_partkey bigint not null, l_linestatus char(1) null, l_tax money not null, l_commitdate date null, l_receiptdate date null, l_shipmode char(10) null, l_linenumber bigint not null, l_shipinstruct char(25) null, l_comment varchar(44) null)" 
set sql(3) "create table dbo.nation(n_nationkey int not null, n_name char(25) null, n_regionkey int null, n_comment varchar(152) null)" 
set sql(4) "create table dbo.part( p_partkey bigint not null, p_type varchar(25) null, p_size int null, p_brand char(10) null, p_name varchar(55) null, p_container char(10) null, p_mfgr char(25) null, p_retailprice money null, p_comment varchar(23) null)" 
set sql(5) "create table dbo.partsupp( ps_partkey bigint not null, ps_suppkey int not null, ps_supplycost money not null, ps_availqty int null, ps_comment varchar(199) null)" 
set sql(6) "create table dbo.region(r_regionkey int not null, r_name char(25) null, r_comment varchar(152) null)"
set sql(7) "create table dbo.supplier( s_suppkey int not null, s_nationkey int null, s_comment varchar(102) null, s_name char(25) null, s_address varchar(40) null, s_phone char(15) null, s_acctbal money null)" 
set sql(8) "create table dbo.orders( o_orderdate date null, o_orderkey bigint not null, o_custkey bigint not null, o_orderpriority char(15) null, o_shippriority int null, o_clerk char(15) null, o_orderstatus char(1) null, o_totalprice money null, o_comment varchar(79) null)"
}
for { set i 1 } { $i <= 8 } { incr i } {
$odbc evaldirect $sql($i)
		}
return
	}

proc CreateIndexes { odbc maxdop colstore } {
puts "CREATING TPCH INDEXES"
if { $colstore } {
set sql(1) "create unique index nation_pk on dbo.nation(n_nationkey)"
set sql(2) "create unique index region_pk on dbo.region(r_regionkey)"
set sql(3) "create unique index customer_pk on dbo.customer(c_custkey) with (maxdop=$maxdop)"
set sql(4) "create unique index part_pk on dbo.part(p_partkey) with (maxdop=$maxdop)"
set sql(5) "create unique index partsupp_pk on dbo.partsupp(ps_partkey, ps_suppkey) with (maxdop=$maxdop)"
set sql(6) "create unique index supplier_pk on dbo.supplier(s_suppkey) with (maxdop=$maxdop)"
set sql(7) "create index o_orderdate_ind on orders(o_orderdate) with (fillfactor=95, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(8) "create unique index orders_pk on dbo.orders(o_orderkey) with (fillfactor = 95, maxdop=$maxdop)"
set sql(9) "create index n_regionkey_ind on dbo.nation(n_regionkey) with (fillfactor=100, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(10) "create index ps_suppkey_ind on dbo.partsupp(ps_suppkey) with(fillfactor=100, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(11) "create index s_nationkey_ind on dbo.supplier(s_nationkey) with (fillfactor=100, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(12) "create index l_shipdate_ind on dbo.lineitem(l_shipdate) with (fillfactor=95, sort_in_tempdb=off, maxdop=$maxdop)"
set sql(13) "create index l_orderkey_ind on dbo.lineitem(l_orderkey) with ( fillfactor=95, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(14) "create index l_partkey_ind on dbo.lineitem(l_partkey) with (fillfactor=95, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(15) "alter table dbo.customer with nocheck add  constraint customer_nation_fk foreign key(c_nationkey) references dbo.nation (n_nationkey)"
set sql(16) "alter table dbo.lineitem with nocheck add  constraint lineitem_order_fk foreign key(l_orderkey) references dbo.orders (o_orderkey)"
set sql(17) "alter table dbo.lineitem with nocheck add constraint lineitem_partkey_fk foreign key (l_partkey) references dbo.part(p_partkey)"
set sql(18) "alter table dbo.lineitem with nocheck add constraint lineitem_suppkey_fk foreign key (l_suppkey) references dbo.supplier(s_suppkey)"
set sql(19) "alter table dbo.lineitem with nocheck add  constraint lineitem_partsupp_fk foreign key(l_partkey,l_suppkey) references partsupp(ps_partkey, ps_suppkey)"
set sql(20) "alter table dbo.nation  with nocheck add  constraint nation_region_fk foreign key(n_regionkey) references dbo.region (r_regionkey)"
set sql(21) "alter table dbo.partsupp  with nocheck add  constraint partsupp_part_fk foreign key(ps_partkey) references dbo.part (p_partkey)"
set sql(22) "alter table dbo.partsupp  with nocheck add  constraint partsupp_supplier_fk foreign key(ps_suppkey) references dbo.supplier (s_suppkey)"
set sql(23) "alter table dbo.supplier  with nocheck add  constraint supplier_nation_fk foreign key(s_nationkey) references dbo.nation (n_nationkey)"
set sql(24) "alter table dbo.orders  with nocheck add  constraint order_customer_fk foreign key(o_custkey) references dbo.customer (c_custkey)"
set sql(25) "alter table dbo.customer check constraint customer_nation_fk"
set sql(26) "alter table dbo.lineitem check constraint lineitem_order_fk"
set sql(27) "alter table dbo.lineitem check constraint lineitem_partkey_fk"
set sql(28) "alter table dbo.lineitem check constraint lineitem_suppkey_fk"
set sql(29) "alter table dbo.lineitem check constraint lineitem_partsupp_fk"
set sql(30) "alter table dbo.nation check constraint nation_region_fk"
set sql(31) "alter table dbo.partsupp check constraint partsupp_part_fk"
set sql(32) "alter table dbo.partsupp check constraint partsupp_part_fk"
set sql(33) "alter table dbo.supplier check constraint supplier_nation_fk"
set sql(34) "alter table dbo.orders check constraint order_customer_fk"
	} else {
set sql(1) "alter table dbo.nation add constraint nation_pk primary key (n_nationkey)"
set sql(2) "alter table dbo.region add constraint region_pk primary key (r_regionkey)"
set sql(3) "alter table dbo.customer add constraint customer_pk primary key (c_custkey) with (maxdop=$maxdop)"
set sql(4) "alter table dbo.part add constraint part_pk primary key (p_partkey) with (maxdop=$maxdop)"
set sql(5) "alter table dbo.partsupp add constraint partsupp_pk primary key (ps_partkey, ps_suppkey) with (maxdop=$maxdop)"
set sql(6) "alter table dbo.supplier add constraint supplier_pk primary key (s_suppkey) with (maxdop=$maxdop)"
set sql(7) "create clustered index o_orderdate_ind on orders(o_orderdate) with (fillfactor=95, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(8) "alter table dbo.orders add constraint orders_pk primary key (o_orderkey) with (fillfactor = 95, maxdop=$maxdop)"
set sql(9) "create index n_regionkey_ind on dbo.nation(n_regionkey) with (fillfactor=100, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(10) "create index ps_suppkey_ind on dbo.partsupp(ps_suppkey) with(fillfactor=100, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(11) "create index s_nationkey_ind on dbo.supplier(s_nationkey) with (fillfactor=100, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(12) "create clustered index l_shipdate_ind on dbo.lineitem(l_shipdate) with (fillfactor=95, sort_in_tempdb=off, maxdop=$maxdop)"
set sql(13) "create index l_orderkey_ind on dbo.lineitem(l_orderkey) with ( fillfactor=95, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(14) "create index l_partkey_ind on dbo.lineitem(l_partkey) with (fillfactor=95, sort_in_tempdb=on, maxdop=$maxdop)"
set sql(15) "alter table dbo.customer with nocheck add  constraint customer_nation_fk foreign key(c_nationkey) references dbo.nation (n_nationkey)"
set sql(16) "alter table dbo.lineitem with nocheck add  constraint lineitem_order_fk foreign key(l_orderkey) references dbo.orders (o_orderkey)"
set sql(17) "alter table dbo.lineitem with nocheck add constraint lineitem_partkey_fk foreign key (l_partkey) references dbo.part(p_partkey)"
set sql(18) "alter table dbo.lineitem with nocheck add constraint lineitem_suppkey_fk foreign key (l_suppkey) references dbo.supplier(s_suppkey)"
set sql(19) "alter table dbo.lineitem with nocheck add  constraint lineitem_partsupp_fk foreign key(l_partkey,l_suppkey) references partsupp(ps_partkey, ps_suppkey)"
set sql(20) "alter table dbo.nation  with nocheck add  constraint nation_region_fk foreign key(n_regionkey) references dbo.region (r_regionkey)"
set sql(21) "alter table dbo.partsupp  with nocheck add  constraint partsupp_part_fk foreign key(ps_partkey) references dbo.part (p_partkey)"
set sql(22) "alter table dbo.partsupp  with nocheck add  constraint partsupp_supplier_fk foreign key(ps_suppkey) references dbo.supplier (s_suppkey)"
set sql(23) "alter table dbo.supplier  with nocheck add  constraint supplier_nation_fk foreign key(s_nationkey) references dbo.nation (n_nationkey)"
set sql(24) "alter table dbo.orders  with nocheck add  constraint order_customer_fk foreign key(o_custkey) references dbo.customer (c_custkey)"
set sql(25) "alter table dbo.customer check constraint customer_nation_fk"
set sql(26) "alter table dbo.lineitem check constraint lineitem_order_fk"
set sql(27) "alter table dbo.lineitem check constraint lineitem_partkey_fk"
set sql(28) "alter table dbo.lineitem check constraint lineitem_suppkey_fk"
set sql(29) "alter table dbo.lineitem check constraint lineitem_partsupp_fk"
set sql(30) "alter table dbo.nation check constraint nation_region_fk"
set sql(31) "alter table dbo.partsupp check constraint partsupp_part_fk"
set sql(32) "alter table dbo.partsupp check constraint partsupp_part_fk"
set sql(33) "alter table dbo.supplier check constraint supplier_nation_fk"
set sql(34) "alter table dbo.orders check constraint order_customer_fk"
	}
for { set i 1 } { $i <= 34 } { incr i } {
$odbc evaldirect $sql($i)
		}
return
	}

proc mk_region { odbc } {
for { set i 1 } { $i <= 5 } {incr i} {
set code [ expr {$i - 1} ]
set text [ lindex [ lindex [ get_dists regions ] [ expr {$i - 1} ] ] 0 ]
set comment [ TEXT_1 72 ]
$odbc evaldirect "INSERT INTO region (r_regionkey,r_name,r_comment) VALUES ('$code' , '$text' , '$comment')"
	}
 }

proc mk_nation { odbc } {
for { set i 1 } { $i <= 25 } {incr i} {
set code [ expr {$i - 1} ]
set text [ lindex [ lindex [ get_dists nations ] [ expr {$i - 1} ] ] 0 ]
set nind [ lsearch -glob [ get_dists nations ] \*$text\* ]
switch $nind {
0 - 4 - 5 - 14 - 15 - 16 { set join 0 }
1 - 2 - 3 - 17 - 24 { set join 1 }
8 - 9 - 12 - 18 - 21 { set join 2 }
6 - 7 - 19 - 22 - 23 { set join 3 }
10 - 11 - 13 - 20 { set join 4 }
}
set comment [ TEXT_1 72 ]
$odbc evaldirect "INSERT INTO nation (n_nationkey, n_name, n_regionkey, n_comment) VALUES ('$code' , '$text' , '$join' , '$comment')"
	}
}

proc mk_supp { odbc start_rows end_rows } {
set bld_cnt 1
set BBB_COMMEND   "Recommends"
set BBB_COMPLAIN  "Complaints"
for { set i $start_rows } { $i <= $end_rows } { incr i } {
set suppkey $i
set name [ concat Supplier#[format %1.9d $i]]
set address [ V_STR 25 ]
set nation_code [ RandomNumber 0 24 ]
set phone [ gen_phone ]
#random format to 2 floating point places 1681.00
set acctbal [format %4.2f [ expr {[ expr {double([ RandomNumber -99999 999999 ])} ] / 100} ] ]
set comment [ TEXT_1 63 ]
set bad_press [ RandomNumber 1 10000 ]
set type [ RandomNumber 0 100 ]
set noise [ RandomNumber 0 19 ]
set offset [ RandomNumber 0 [ expr {19 + $noise} ] ]
if { $bad_press <= 10 } {
set st [ expr {9 + $offset + $noise} ]
set fi [ expr {$st + 10} ]
if { $type < 50 } {
set comment [ string replace $comment $st $fi $BBB_COMPLAIN ]
} else {
set comment [ string replace $comment $st $fi $BBB_COMMEND ]
	}
}
append supp_val_list ('$suppkey', '$nation_code', '$comment', '$name', '$address', '$phone', '$acctbal')
incr bld_cnt
if { ![ expr {$i % 2} ] || $i eq $end_rows } {    
$odbc evaldirect "INSERT INTO supplier (s_suppkey, s_nationkey, s_comment, s_name, s_address, s_phone, s_acctbal) VALUES $supp_val_list"
	set bld_cnt 1
	unset supp_val_list
	} else {
	append supp_val_list ,
        }
if { ![ expr {$i % 10000} ] } {
	puts "Loading SUPPLIER...$i"
	}
   }
puts "SUPPLIER Done Rows $start_rows..$end_rows"
return
}

proc mk_cust { odbc start_rows end_rows } {
set bld_cnt 1
for { set i $start_rows } { $i <= $end_rows } { incr i } {
set custkey $i
set name [ concat Customer#[format %1.9d $i]]
set address [ V_STR 25 ]
set nation_code [ RandomNumber 0 24 ]
set phone [ gen_phone ]
set acctbal [format %4.2f [ expr {[ expr {double([ RandomNumber -99999 999999 ])} ] / 100} ] ]
set mktsegment [ pick_str_1 msegmnt ]
set comment [ TEXT_1 73 ]
append cust_val_list ('$custkey', '$mktsegment', '$nation_code', '$name', '$address', '$phone', '$acctbal', '$comment') 
incr bld_cnt
if { ![ expr {$i % 2} ] || $i eq $end_rows } {    
$odbc evaldirect "INSERT INTO customer (c_custkey, c_mktsegment, c_nationkey, c_name, c_address, c_phone, c_acctbal, c_comment) values $cust_val_list"
	set bld_cnt 1
	unset cust_val_list
   	} else {
	append cust_val_list ,
        }
if { ![ expr {$i % 10000} ] } {
	puts "Loading CUSTOMER...$i"
	}
}
puts "CUSTOMER Done Rows $start_rows..$end_rows"
return
}

proc mk_part { odbc start_rows end_rows scale_factor } {
set bld_cnt 1
for { set i $start_rows } { $i <= $end_rows } { incr i } {
set partkey $i
unset -nocomplain name
for {set j 0} {$j < [ expr {5 - 1} ] } {incr j } {
append name [ pick_str_1 colors ] " "
}
append name [ pick_str_1 colors ]
set mf [ RandomNumber 1 5 ]
set mfgr [ concat Manufacturer#$mf ]
set brand [ concat Brand#[ expr {$mf * 10 + [ RandomNumber 1 5 ]} ] ]
set type [ pick_str_1 p_types ] 
set size [ RandomNumber 1 50 ]
set container [ pick_str_1 p_cntr ] 
set price [ rpb_routine $i ]
set comment [ TEXT_1 14 ]
append part_val_list ('$partkey', '$type', '$size', '$brand', '$name', '$container', '$mfgr', '$price', '$comment')
#Part Supp Loop
for {set k 0} {$k < 4 } {incr k } {
set psupp_pkey $partkey
set psupp_suppkey [ PART_SUPP_BRIDGE $i $k $scale_factor ]
set psupp_qty [ RandomNumber 1 9999 ]
set psupp_scost [format %4.2f [ expr {double([ RandomNumber 100 100000 ]) / 100} ] ]
set psupp_comment [ TEXT_1 124 ]
append psupp_val_list ('$psupp_pkey', '$psupp_suppkey', '$psupp_scost', '$psupp_qty', '$psupp_comment') 
if { $k<=2 } { 
append psupp_val_list ,
	}
}
incr bld_cnt
# end of psupp loop
if { ![ expr {$i % 2} ]  || $i eq $end_rows } {     
$odbc evaldirect "INSERT INTO part (p_partkey, p_type, p_size, p_brand, p_name, p_container, p_mfgr, p_retailprice, p_comment) VALUES $part_val_list"
$odbc evaldirect "INSERT INTO partsupp (ps_partkey, ps_suppkey, ps_supplycost, ps_availqty, ps_comment) VALUES $psupp_val_list"
	set bld_cnt 1
	unset part_val_list
	unset psupp_val_list
	} else {
	append psupp_val_list ,
	append part_val_list ,
	}
if { ![ expr {$i % 10000} ] } {
	puts "Loading PART/PARTSUPP...$i"
	}
}
puts "PART and PARTSUPP Done Rows $start_rows..$end_rows"
return
}

proc mk_order { odbc start_rows end_rows upd_num scale_factor } {
set bld_cnt 1
set refresh 100
set delta 1
set L_PKEY_MAX   [ expr {200000 * $scale_factor} ]
set O_CKEY_MAX [ expr {150000 * $scale_factor} ]
set O_ODATE_MAX [ expr {(92001 + 2557 - (121 + 30) - 1)} ]
for { set i $start_rows } { $i <= $end_rows } { incr i } {
if { $upd_num == 0 } {
set okey [ mk_sparse $i $upd_num ]
} else {
set okey [ mk_sparse $i [ expr {1 + $upd_num / (10000 / $refresh)} ] ]
}
set custkey [ RandomNumber 1 $O_CKEY_MAX ]
while { $custkey % 3 == 0 } {
set custkey [ expr {$custkey + $delta} ]
if { $custkey < $O_CKEY_MAX } { set min $custkey } else { set min $O_CKEY_MAX }
set custkey $min
set delta [ expr {$delta * -1} ]
}
if { ![ array exists ascdate ] } {
for { set d 1 } { $d <= 2557 } {incr d} {
set ascdate($d) [ mk_time $d ]
	}
}
set tmp_date [ RandomNumber 92002 $O_ODATE_MAX ]
set date $ascdate([ expr {$tmp_date - 92001} ])
set opriority [ pick_str_1 o_oprio ] 
set clk_num [ RandomNumber 1 [ expr {$scale_factor * 1000} ] ]
set clerk [ concat Clerk#[format %1.9d $clk_num]]
set comment [ TEXT_1 49 ]
set spriority 0
set totalprice 0
set orderstatus "O"
set ocnt 0
set lcnt [ RandomNumber 1 7 ]
#Lineitem Loop
for { set l 0 } { $l < $lcnt } {incr l} {
set lokey $okey
set llcnt [ expr {$l + 1} ]
set lquantity [ RandomNumber 1 50 ]
set ldiscount [format %1.2f [ expr [ RandomNumber 0 10 ] / 100.00 ]]
set ltax [format %1.2f [ expr [ RandomNumber 0 8 ] / 100.00 ]]
set linstruct [ pick_str_1 instruct ] 
set lsmode [ pick_str_1 smode ] 
set lcomment [ TEXT_1 27 ]
set lpartkey [ RandomNumber 1 $L_PKEY_MAX ]
set rprice [ rpb_routine $lpartkey ]
set supp_num [ RandomNumber 0 3 ]
set lsuppkey [ PART_SUPP_BRIDGE $lpartkey $supp_num $scale_factor ]
set leprice [format %4.2f [ expr {$rprice * $lquantity} ]]
set totalprice [format %4.2f [ expr {$totalprice + [ expr {(($leprice * (100 - $ldiscount)) / 100) * (100 + $ltax) / 100} ]}]]
set s_date [ RandomNumber 1 121 ]
set s_date [ expr {$s_date + $tmp_date} ] 
set c_date [ RandomNumber 30 90 ]
set c_date [ expr {$c_date + $tmp_date} ]
set r_date [ RandomNumber 1 30 ]
set r_date [ expr {$r_date + $s_date} ]
set lsdate $ascdate([ expr {$s_date - 92001} ])
set lcdate $ascdate([ expr {$c_date - 92001} ])
set lrdate $ascdate([ expr {$r_date - 92001} ])
if { [ julian $r_date ] <= 95168 } {
set lrflag [ pick_str_1 rflag ] 
} else { set lrflag "N" }
if { [ julian $s_date ] <= 95168 } {
incr ocnt
set lstatus "F"
} else { set lstatus "O" }
append lineit_val_list ('$lsdate','$lokey', '$ldiscount', '$leprice', '$lsuppkey', '$lquantity', '$lrflag', '$lpartkey', '$lstatus', '$ltax', '$lcdate', '$lrdate', '$lsmode', '$llcnt', '$linstruct', '$lcomment') 
if { $l < [ expr $lcnt - 1 ] } { 
append lineit_val_list ,
	} 
  }
if { $ocnt > 0} { set orderstatus "P" }
if { $ocnt == $lcnt } { set orderstatus "F" }
append order_val_list ('$date', '$okey', '$custkey', '$opriority', '$spriority', '$clerk', '$orderstatus', '$totalprice', '$comment') 
incr bld_cnt
if { ![ expr {$i % 2} ]  || $i eq $end_rows } {     
$odbc evaldirect "INSERT INTO lineitem (l_shipdate, l_orderkey, l_discount, l_extendedprice, l_suppkey, l_quantity, l_returnflag, l_partkey, l_linestatus, l_tax, l_commitdate, l_receiptdate, l_shipmode, l_linenumber, l_shipinstruct, l_comment) VALUES $lineit_val_list"
$odbc evaldirect "INSERT INTO orders (o_orderdate, o_orderkey, o_custkey, o_orderpriority, o_shippriority, o_clerk, o_orderstatus, o_totalprice, o_comment) VALUES $order_val_list"
	set bld_cnt 1
	unset lineit_val_list
	unset order_val_list
   	} else {
	append order_val_list ,
	append lineit_val_list ,
	}
if { ![ expr {$i % 10000} ] } {
	puts "Loading ORDERS/LINEITEM...$i"
	}
}
puts "ORDERS and LINEITEM Done Rows $start_rows..$end_rows"
return
}

proc connect_string { server port odbc_driver authentication uid pwd tcp azure db } {
if { $tcp eq "true" } { set server tcp:$server,$port }
if {[ string toupper $authentication ] eq "WINDOWS" } {
set connection "DRIVER=$odbc_driver;SERVER=$server;TRUSTED_CONNECTION=YES"
} else {
if {[ string toupper $authentication ] eq "SQL" } {
set connection "DRIVER=$odbc_driver;SERVER=$server;UID=$uid;PWD=$pwd"
        } else {
puts stderr "Error: neither WINDOWS or SQL Authentication has been specified"
set connection "DRIVER=$odbc_driver;SERVER=$server"
        }
}
if { $azure eq "true" } { append connection ";" "DATABASE=$db" }
return $connection
}

proc do_tpch { server port scale_fact odbc_driver authentication uid pwd tcp azure db maxdop colstore num_vu } {
global dist_names dist_weights weights dists weights
###############################################
#Generating following rows
#5 rows in region table
#25 rows in nation table
#SF * 10K rows in Supplier table
#SF * 150K rows in Customer table
#SF * 200K rows in Part table
#SF * 800K rows in Partsupp table
#SF * 1500K rows in Orders table
#SF * 6000K rows in Lineitem table
###############################################
set connection [ connect_string $server $port $odbc_driver $authentication $uid $pwd $tcp $azure $db ]
#update number always zero for first load
set upd_num 0
if { ![ array exists dists ] } { set_dists }
foreach i [ array names dists ] {
set_dist_list $i
}
set sup_rows [ expr {$scale_fact * 10000} ]
set max_threads 256
set sf_mult 1
set cust_mult 15
set part_mult 20
set ord_mult 150
if { $num_vu > $max_threads } { set num_vu $max_threads }
if { $num_vu > 1 && [ chk_thread ] eq "TRUE" } {
set threaded "MULTI-THREADED"
set rema [ lassign [ findvuhposition ] myposition totalvirtualusers ]
switch $myposition {
	1 { 
puts "Monitor Thread"
if { $threaded eq "MULTI-THREADED" } {
tsv::lappend common thrdlst monitor
for { set th 1 } { $th <= $totalvirtualusers } { incr th } {
tsv::lappend common thrdlst idle
			}
tsv::set application load "WAIT"
		}
	}
	default { 
puts "Worker Thread"
if { [ expr $myposition - 1 ] > $max_threads } { puts "No Data to Create"; return }
     }
   }
} else {
set threaded "SINGLE-THREADED"
set num_vu 1
  }
if { $threaded eq "SINGLE-THREADED" ||  $threaded eq "MULTI-THREADED" && $myposition eq 1 } {
puts "CREATING [ string toupper $db ] SCHEMA"
if [catch {tdbc::odbc::connection create odbc $connection} message ] {
error "Connection to $connection could not be established : $message"
 } else {
CreateDatabase odbc $db $azure
if {!$azure} {odbc evaldirect "use $db"}
CreateTables odbc $colstore
}
if { $threaded eq "MULTI-THREADED" } {
tsv::set application load "READY"
puts "Loading REGION..."
mk_region odbc
puts "Loading REGION COMPLETE"
puts "Loading NATION..."
mk_nation odbc
puts "Loading NATION COMPLETE"
puts "Monitoring Workers..."
after 10000
set prevactive 0
while 1 {
set idlcnt 0; set lvcnt 0; set dncnt 0;
for {set th 2} {$th <= $totalvirtualusers } {incr th} {
switch [tsv::lindex common thrdlst $th] {
idle { incr idlcnt }
active { incr lvcnt }
done { incr dncnt }
        }
}
if { $lvcnt != $prevactive } {
puts "Workers: $lvcnt Active $dncnt Done"
        }
set prevactive $lvcnt
if { $dncnt eq [expr  $totalvirtualusers - 1] } { break }
after 10000
}} else {
puts "Loading REGION..."
mk_region odbc
puts "Loading REGION COMPLETE"
puts "Loading NATION..."
mk_nation odbc
puts "Loading NATION COMPLETE"
}}
if { $threaded eq "SINGLE-THREADED" ||  $threaded eq "MULTI-THREADED" && $myposition != 1 } {
if { $threaded eq "MULTI-THREADED" } {
puts "Waiting for Monitor Thread..."
set mtcnt 0
while 1 {
if { [ tsv::exists application load ] } {
incr mtcnt
if {  [ tsv::get application load ] eq "READY" } { break }
if {  [ tsv::get application abort ]  } { return }
if { $mtcnt eq 48 } {
puts "Monitor failed to notify ready state"
return
        }
}
after 5000
}
if [catch {tdbc::odbc::connection create odbc $connection} message ] {
error "Connection to $connection could not be established : $message"
 } else {
if {!$azure} {odbc evaldirect "use $db"}
odbc evaldirect "set implicit_transactions OFF"
} 
if { [ expr $myposition - 1 ] > $max_threads } { puts "No Data to Create"; return }
if { [ expr $num_vu + 1 ] > $max_threads } { set num_vu $max_threads }
set sf_chunk [ split [ start_end $sup_rows $myposition $sf_mult $num_vu ] ":" ]
set cust_chunk [ split [ start_end $sup_rows $myposition $cust_mult $num_vu ] ":" ]
set part_chunk [ split [ start_end $sup_rows $myposition $part_mult $num_vu ] ":" ]
set ord_chunk [ split [ start_end $sup_rows $myposition $ord_mult $num_vu ] ":" ]
tsv::lreplace common thrdlst $myposition $myposition active
} else {
set sf_chunk "1 $sup_rows"
set cust_chunk "1 [ expr {$sup_rows * $cust_mult} ]" 
set part_chunk "1 [ expr {$sup_rows * $part_mult} ]" 
set ord_chunk "1 [ expr {$sup_rows * $ord_mult} ]"
}
puts "Start:[ clock format [ clock seconds ] ]"
puts "Loading SUPPLIER..."
mk_supp odbc [ lindex $sf_chunk 0 ] [ lindex $sf_chunk 1 ]
puts "Loading CUSTOMER..."
mk_cust odbc [ lindex $cust_chunk 0 ] [ lindex $cust_chunk 1 ]
puts "Loading PART and PARTSUPP..."
mk_part odbc [ lindex $part_chunk 0 ] [ lindex $part_chunk 1 ] $scale_fact
puts "Loading ORDERS and LINEITEM..."
mk_order odbc [ lindex $ord_chunk 0 ] [ lindex $ord_chunk 1 ] [ expr {$upd_num % 10000} ] $scale_fact 
puts "Loading TPCH TABLES COMPLETE"
puts "End:[ clock format [ clock seconds ] ]"
if { $threaded eq "MULTI-THREADED" } {
tsv::lreplace common thrdlst $myposition $myposition done
        }
}
if { $threaded eq "SINGLE-THREADED" || $threaded eq "MULTI-THREADED" && $myposition eq 1 } {
CreateIndexes odbc $maxdop $colstore
UpdateStatistics odbc $db $azure
puts "[ string toupper $db ] SCHEMA COMPLETE"
odbc close
return
		}
	}
do_tpch {(local)} 1433 1 {ODBC Driver 17 for SQL Server} windows sa admin false false tpch 2 false 8

```

