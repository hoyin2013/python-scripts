select c.id , c.reg_status, c.name as mercRegNm, c.business_scope as businessScope , c.reg_location as regAddr, c.reg_number as regNo, '6432' as cupCode ,
c. legal_person_name as legalNm, c.property1 as socialCreditCode, c.from_time as licenseEffStartdate , c.to_time as licenseEffEnddate ,c.reg_capital as regCapital,
'白沙黎族自治县' as city  from
company c where c.base ='han' and c.reg_location like '%白沙黎族自治县%'
and c.reg_status in ('开业','存续','存续（在营、开业、在册）','在业','在营（开业）','在营','正常','个体转企业','在营（开业）企业')
and  c.to_time is not null  and ( c.name not like '%医院%' or c.name not like '%金融%'
or c.name not like '%房地产%' or c.name not like '%殡仪馆%'
or c.name not like'%银行%'
) limit 1,20000