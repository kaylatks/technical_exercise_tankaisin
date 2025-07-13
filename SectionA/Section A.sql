--Question 1-Display student’s ID and name who at least have one similar course with student ID “01”.
select distinct stu.s_id id,stu.s_name 
from student stu left join score s on stu.s_id = s.s_id 
where s.c_id in (select c_id from score s where s_id = '01')
	and stu.s_id <> '01'
	

-- Question 2 - Create segment for course score [100-85], [85-70], [70-60], [<60] and count number of students under those segments for all courses, column to display also are course ID and course name.
--with segment_cte as (
--select s_id,c_id,s_score 
--	,case when s_score >=85 and s_score <=100 then '[100-85]'
--		when s_score >=70 and s_score <85 then '[85-70]'
--		when s_score >=60 and s_score <70 then '[70-60]'
--		when s_score <60 then '[<60]' end as segment
--from score s
--)
--select s.c_id,c.c_name ,s.segment,count(s.s_id) 
--from segment_cte s left join course c on s.c_id = c.c_id 
--group by s.c_id,c.c_name ,s.segment
--order by s.c_id 
	
	
--CREATE TABLE score_segments (
--  segment_label TEXT,
--  min_score INT,
--  max_score INT
--);
--insert into score_segments values('[100-85]',85,100);
--insert into score_segments values('[85-70]',70,84);
--insert into score_segments values('[70-60]',60,69);
--insert into score_segments values('[<60]',0,59);

select s.c_id ,c.c_name ,ss.segment_label , count(s.s_id) 
from score s 
	join score_segments ss on s.s_score between ss.min_score and ss.max_score
	left join course c on s.c_id = c.c_id 
group by s.c_id,c.c_name ,ss.segment_label
order by s.c_id 

--Question3 - Display student ID, course ID and student score where student has the same score but in different course.
select s1.s_id ,s1.c_id ,s1.s_score 
from score s1 
where exists (
	select 1
	from score s2
	where s1.s_id = s2.s_id 
		and s1.s_score = s2.s_score 
		and s1.c_id <> s2.c_id 
)
order by s1.s_id ,s1.c_id ,s1.s_score 


--Question4 - Query for the top 2 highest in scoring from each course and display column course ID, course name, student name and student score.
with score_ranking_cte as (
select s.s_id ,s.c_id ,s.s_score ,dense_rank () over(partition by s.c_id order by s.s_score DESC) as rn
from score s 
)
select c.c_id ,c.c_name ,s.s_name, cte.s_score 
from score_ranking_cte cte 
	left join course c on cte.c_id = c.c_id 
	left join student s on cte.s_id = s.s_id 
where rn<=2

--Question5 - Query for all student’s information that has registered for all courses.
with student_course_taken_cte as (
select s.s_id ,count(s.c_id) as no_course_taken
from score s
group by s.s_id
)
select distinct stu.* 
from student stu 
	left join score sc on stu.s_id = sc.s_id 
	left join student_course_taken_cte cte on stu.s_id = cte.s_id
where cte.no_course_taken = (select count(c_id) from course)



