-- Shows results of albums where their id is either 1 or 2:
-- select * from albums
-- where AlbumId = 1 or AlbumId = 2;

-- Shows results of albums if both conditions are true:
-- select * from albums
-- where AlbumId = 1 and ArtistId = 1;

-- Shows results of albums between 1(begin) and 10(end):
-- select * from albums
-- where AlbumId between 1 and 10;

-- Shows results of matching values in both tables:
-- select albums.ArtistId, albums.Title, artists.Name from albums
-- join artists ON albums.ArtistId = artists.ArtistId;

-- Shows results of all rows from left table, which in this case is albums, even if there are no matches in right table:
-- select albums.ArtistId, albums.Title, artists.Name from albums
-- left join artists ON albums.ArtistId = artists.ArtistId;

-- Same as left join but instead will show all rows from right table, which in this case is artists:
-- select albums.ArtistId, albums.Title, artists.Name from albums
-- right join artists ON albums.ArtistId = artists.ArtistId;

-- Union combines two or more SELECT statements but both statements must have same number of columns, data types and need to be in the same order:
-- Union also only shows unique values. To show duplicates too, use UNION ALL:
-- select ArtistId from albums
-- union
-- select ArtistId from artists;

-- COALESCE will return first value that is not NULL, in below example it would return 1;
-- select coalesce(NULL, NULL, 1, 2, 3);

-- CASE will return value if conditions are met, similarly to IF-ELIF-ELSE in Python:
-- select ArtistId,
-- case
-- 	when ArtistId != 1 then ArtistId
--     else "Can't return artist id 1"
-- end
-- from albums;

-- ORDER BY is used to sort values. By default it sorts in ascending order to sort in descending: ORDER BY ArtistId ASC/DESC;
-- select * from albums
-- order by Title desc;

-- LIMIT is used to specify how many rows to return. OFFSET is used to point from where to start showing rows limited rows;
-- select * from albums limit 10 offset 20;

-- In PROCEDURE you can store a set of statements, call it to execute and return results.
-- DELIMITER is closing for each statement by default its semicolon(;) but if you want to write (;) without mysql thinking you're done with it then change delimiter to something as shown below:

-- delimiter $$

-- create procedure get_all_albums()
-- begin
-- 	select *  from albums;
-- end $$

-- delimiter ;

-- call get_all_albums();

-- FUNCTION is similar to PROCEDURE but it must return values while procedure doesn't
-- FUNCTION only can have input parameters while PROCEDURE can have input and output parameters
-- FUNCTION can be called from PROCEDURE while PROCEDURE cant be called from FUNCTION

-- delimiter $$

-- create function album_based_on_length(album_title nvarchar(99), desired_length integer)
-- returns nvarchar(20)
-- deterministic
-- begin
-- 	declare album_returned nvarchar(20);
--     if length(album_title) < desired_length then set album_returned = album_title;
--     end if;
--     return (album_returned);
-- end $$

-- delimiter ;

-- select AlbumId, album_based_on_length(Title, 20) from albums;