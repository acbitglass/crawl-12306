-- 创建测试数据


--创建学生表 student
drop table if exists student;
create table if not exists student(
sid int comment '学生ID',
sname varchar(10) comment '学生姓名',
sage datetime comment '出生年月',
ssex varchar(10) comment '性别'
);
--插入数据
insert into Student values('01' , '赵雷' , '1990-01-01' , '男');
insert into Student values('02' , '钱电' , '1990-12-21' , '男');
insert into Student values('03' , '孙风' , '1990-05-20' , '男');
insert into Student values('04' , '李云' , '1990-08-06' , '男');
insert into Student values('05' , '周梅' , '1991-12-01' , '女');
insert into Student values('06' , '吴兰' , '1992-03-01' , '女');
insert into Student values('07' , '郑竹' , '1989-07-01' , '女');
insert into Student values('09' , '张三' , '2017-12-20' , '女');
insert into Student values('10' , '李四' , '2017-12-25' , '女');
insert into Student values('11' , '李四' , '2017-12-30' , '女');
insert into Student values('12' , '赵六' , '2017-01-01' , '女');
insert into Student values('13' , '孙七' , '2018-01-01' , '女');

--创建科目表
drop table if exists course;
create table if not exists course(
cid int comment '课程ID',
cname varchar(10) comment '课程名称',
tid int comment '教师ID'
);
--插入数据
insert into course values('01' , '语文' , '02');
insert into course values('02' , '数学' , '01');
insert into course values('03' , '英语' , '03');

--创建教师表
drop table if exists teacher;
create table if not exists teacher(
tid int comment '教师ID',
tname varchar(10) comment '教师姓名'
);
--插入数据
insert into teacher values('01' , '张三');
insert into teacher values('02' , '李四');
insert into teacher values('03' , '王五');

--创建成绩表
drop table if exists sc;
create table if not exists sc(
sid int comment '学生ID',
cid int comment '课程ID',
score decimal(18,1) comment '份数'
);
--插入数据
insert into sc values('01' , '01' , 80);
insert into sc values('01' , '02' , 90);
insert into sc values('01' , '03' , 99);
insert into sc values('02' , '01' , 70);
insert into sc values('02' , '02' , 60);
insert into sc values('02' , '03' , 80);
insert into sc values('03' , '01' , 80);
insert into sc values('03' , '02' , 80);
insert into sc values('03' , '03' , 80);
insert into sc values('04' , '01' , 50);
insert into sc values('04' , '02' , 30);
insert into sc values('04' , '03' , 20);
insert into sc values('05' , '01' , 76);
insert into sc values('05' , '02' , 87);
insert into sc values('06' , '01' , 31);
insert into sc values('06' , '03' , 34);
insert into sc values('07' , '02' , 89);
insert into sc values('07' , '03' , 98);


--练习题目
# 1. 查询" 01 "课程比" 02 "课程成绩高的学生的信息及课程分数
select a.sid, c.sname, c.sage, c.ssex, a.score as score1, b.score as score2 from
(select * from sc where cid=01) a
inner join
(select * from sc where cid=02) b on a.sid=b.sid
inner join student c on a.sid=c.sid
where a.score>b.score;
# 1.1 查询同时存在" 01 "课程和" 02 "课程的情况
select a.sid, c.sname, c.sage, c.ssex, a.score as score1, b.score as score2 from
(select * from sc where cid=01) a
inner join
(select * from sc where cid=02) b on a.sid=b.sid
inner join student c on a.sid=c.sid;
# 1.2 查询存在" 01 "课程但可能不存在" 02 "课程的情况(不存在时显示为 null )
select a.sid, c.sname, c.sage, c.ssex, a.score as score1, b.score as score2 from
(select * from sc where cid=01) a
left join
(select * from sc where cid=02) b on a.sid=b.sid
left join student c on a.sid=c.sid;
# 1.3 查询不存在" 01 "课程但存在" 02 "课程的情况
select a.sid, c.sname, c.sage, c.ssex from
(select * from sc where cid=02 and sid not in (select sid from sc where cid=01)) a
left join student c on a.sid=c.sid;
# 2. 查询平均成绩大于等于 60 分的同学的学生编号和学生姓名和平均成绩
select a.sid, b.sname, avg(a.score) from sc a
left join student b on a.sid=b.sid
group by a.sid, b.sname having avg(a.score)>=60;
# 3. 查询在 SC 表存在成绩的学生信息
select * from student where sid in (select sid from sc);
# 4. 查询所有同学的学生编号、学生姓名、选课总数、所有课程的总成绩(没成绩的显示为 null )
select a.sid
,a.sname
,count(distinct cid) 选课总数
,sum(score) 总成绩 from student a left join sc b on a.sid=b.sid
group by a.sid
,a.sname;
# 4.1 查有成绩的学生信息
select a.sid
,a.sname
,count(distinct cid) 选课总数
,sum(score) 总成绩 from student a left join sc b on a.sid=b.sid
group by a.sid
,a.sname
having sum(score) is not null;
# 5. 查询「李」姓老师的数量
select count(*) from teacher where tname like '李%';
# 6. 查询学过「张三」老师授课的同学的信息
select a.tname, d.sname from teacher a
left join course b on a.tid=b.tid
left join sc c on b.cid=c.cid
left join student d on c.sid=d.sid
where a.tname='张三';
# 7. 查询没有学全所有课程的同学的信息
select sid, count(distinct cid) from sc group by sid having count(distinct cid)<(select count(*) from course);
# 8. 查询至少有一门课与学号为" 01 "的同学所学相同的同学的信息
select distinct sid from sc where cid in (select cid from sc where sid=01);
# 9. 查询和" 01 "号的同学学习的课程 完全相同的其他同学的信息
select sid, group_concat(cid) from (select * from sc order by sid, cid) t group by sid having group_concat(cid)=(select group_concat(cid) from (select * from sc order by sid, cid) tt where sid=01 group by sid);  #自己写的

select * from student where student.SId not in (select t1.SId from 
(select student.SId,t.CId from student ,(select sc.CId from sc where sc.SId='01') as t )as t1 
left join sc on t1.SId=sc.SId and t1.CId=sc.CId where sc.CId is null ) and student.SId !='01' # 参考
# 10. 查询没学过"张三"老师讲授的任一门课程的学生姓名
select t1.sname from student t1
left join (select * from sc where cid in (select b.cid from teacher a
left join course b on a.tid=b.tid
where tname='张三')) t2 on t1.sid=t2.sid
where t2.cid is null;
# 11. 查询两门及其以上不及格课程的同学的学号，姓名及其平均成绩
select a.sid, b.avg_score, count(distinct a.cid) 不及格门数 from sc a
left join (select sid, avg(score) avg_score from sc group by sid) b on a.sid=b.sid
where a.score<60 group by a.sid, b.avg_score having count(distinct a.cid)>=2;
# 12. 检索" 01 "课程分数小于 60，按分数降序排列的学生信息
select * from sc where cid=01 and score<60 order by score desc;
# 13. 按平均成绩从高到低显示所有学生的所有课程的成绩以及平均成绩
select a.*, b.avg_score from sc a
left join (select sid, avg(score) avg_score from sc group by sid) b on a.sid=b.sid
order by b.avg_score desc;
# 14. 查询各科成绩最高分、最低分和平均分：
# 以如下形式显示：课程 ID，课程 name，最高分，最低分，平均分，及格率，中等率，优良率，优秀率
# 及格为>=60，中等为：70-80，优良为：80-90，优秀为：>=90
# 要求输出课程号和选修人数，查询结果按人数降序排列，若人数相同，按课程号升序排列
select cid, count(distinct sid) s_num, max(score), min(score), avg(score), 
sum(case when score>=90 then 1 else 0 end)/count(distinct sid) yx,
sum(case when score<90 and score>=80 then 1 else 0 end)/count(distinct sid) yn,
sum(case when score<80 and score>=70 then 1 else 0 end)/count(distinct sid) zd,
sum(case when score<70 and score>=60 then 1 else 0 end)/count(distinct sid) jg,
sum(case when score<60 then 1 else 0 end)/count(distinct sid) bjg
from sc a 
group by cid order by s_num desc, cid;
# 15. 按各科成绩进行排序，并显示排名， Score 重复时保留名次空缺
select sc.SId,sc.CId ,
case when @pre_parent_code=sc.CId then @curRank:=@curRank+1 when @pre_parent_code:=sc.CId then  @curRank:=1  end as rank,sc.score
from (select @curRank:=0,@pre_parent_code:='') as t ,sc
ORDER by sc.CId,sc.score desc; #参考答案
# 17. 统计各科成绩各分数段人数：课程编号，课程名称，[100-85]，[85-70]，[70-60]，[60-0] 及所占百分比
select a.cid, b.cname, 
count(distinct a.sid), 
count(distinct case when score>=85 then sid end) `85-100`,
count(distinct case when score>=70 and score<85 then sid end) `70-85`,
count(distinct case when score>=60 and score<70 then sid end) `60-70`,
count(distinct case when score<60 then sid end) `0-60`
from sc a left join course b on a.cid=b.cid
group by a.cid, b.cname;
# 18. 查询各科成绩前三名的记录
select * from (
select a.sid, a.cid, a.score, sum(case when a.score<b.score then 1 else 0 end) num from sc a inner join sc b on a.cid=b.cid
group by a.sid, a.cid, a.score having sum(case when a.score<b.score then 1 else 0 end)<3) t order by cid, score desc; # 自己写的

select *
from sc  
where  (select count(*) from sc as a where sc.CId =a.CId and  sc.score <a.score )<3
ORDER BY CId asc,sc.score desc; # 参考网上
# 19. 查询每门课程被选修的学生数
select cid,count(distinct sid) from sc group by cid;
# 20. 查询出只选修两门课程的学生学号和姓名
select a.sid,b.sname,count(distinct a.cid) from sc a 
left join student b on a.sid=b.sid
 group by a.sid,b.sname having count(distinct a.cid)=2;
# 21. 查询男生、女生人数
select ssex, count(distinct sid) from student group by ssex;
# 22. 查询名字中含有「风」字的学生信息
select * from student where sname like '%风%';
# 23. 查询同名同性学生名单，并统计同名人数
select sname, ssex, count(*) from student group by sname, ssex having count(*)>=2
# 24. 查询 1990 年出生的学生名单
select * from student where year(sage)='1990';
# 25. 查询每门课程的平均成绩，结果按平均成绩降序排列，平均成绩相同时，按课程编号升序排列
select cid,avg(score) avg_score from sc group by cid order by avg_score desc, cid asc;
# 26. 查询平均成绩大于等于 85 的所有学生的学号、姓名和平均成绩
select a.sid, b.sname, avg(a.score) from sc a 
left join student b on a.sid=b.sid
 group by a.sid, b.sname having avg(a.score)>=85;
# 27. 查询课程名称为「数学」，且分数低于 60 的学生姓名和分数
 select c.sname, b.score from course a left join sc b on a.cid=b.cid left join student c on b.sid=c.sid where a.cname='数学' and b.score<60;
# 28. 查询所有学生的课程及分数情况（存在学生没成绩，没选课的情况）
select a.sname, b.cid, b.score from student a left join sc b on a.sid=b.sid;
# 29. 查询任何一门课程成绩在 70 分以上的姓名、课程名称和分数
select t2.sname, t3.cname, t1.score from (select a.* from sc a inner join (select sid, min(score) from sc group by sid having min(score)>70) b on a.sid=b.sid) t1 left join student t2 on t1.sid=t2.sid left join course t3 on t1.cid=t3.cid order by t2.sname;
# 30. 查询不及格的课程
select distinct b.cname from sc a left join course b on a.cid=b.cid where score<60;
# 31. 查询课程编号为 01 且课程成绩在 80 分以上的学生的学号和姓名
select a.sid, b.sname from sc a left join student b on a.sid=b.sid where cid=1 and score>80;
# 32. 求每门课程的学生人数
select cid, count(*) from sc group by cid;
# 33. 成绩不重复，查询选修「张三」老师所授课程的学生中，成绩最高的学生信息及其成绩
select d.sname, c.score from teacher a left join course b on a.tid=b.tid left join sc c on b.cid=c.cid left join student d on c.sid=d.sid where tname='张三' order by score desc limit 1;
# 35. 查询不同课程成绩相同的学生的学生编号、课程编号、学生成绩
select distinct a.* from sc a,sc b where a.score=b.score and a.cid<>b.cid; # 解法1

select * from sc a where (select count(*) from sc b where a.score=b.score and a.cid<>b.cid)>=2; # 解法2
# 36. 查询每门功成绩最好的前两名
select cid, sid, score from sc a where (select count(*) from sc b where a.score<b.score and a.cid=b.cid)<2 order by cid;
# 37. 统计每门课程的学生选修人数（超过 5 人的课程才统计）。
select cid, count(*) from sc group by cid having count(*)>=5;
# 38. 检索至少选修两门课程的学生学号
select sid, count(*) from sc group by sid having count(*)>=2;
# 39. 查询选修了全部课程的学生信息
select sid, count(*) from sc group by sid having count(*)=(select count(*) from course); 
# 40. 查询各学生的年龄，只按年份来算
SELECT sname, sage, timestampdiff(year,sage, date_format(now(), '%Y-%m-%d')) age from student;
# 41. 按照出生日期来算，当前月日 < 出生年月的月日则，年龄减一

# 42. 查询本周过生日的学生
select * from student where week(sage)=week(now());
# 43. 查询下周过生日的学生
select * from student where week(sage)=week(now())+1;
# 44. 查询本月过生日的学生
select * from student where month(sage)=month(now());
# 45. 查询下月过生日的学生
select * from student where month(sage)=month(now())+1;

