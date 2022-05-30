create Database Socket_Account
go

use Socket_Account
go


create table Account(
	username varchar(10) NOT NULL,
	pass varchar(10) NOT NULL,
)

go

insert Account values ('tan1',123456)
insert Account values ('tan2',1234567)
insert Account values ('tan3',1234568)