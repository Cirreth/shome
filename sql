#test skipped records
select * from temperature tl
join
select * from temperature tr
on tl.id = tr.id+1 and tl.sensor_tag = tr.sensor_tag and (tl.time -tr.time)<60