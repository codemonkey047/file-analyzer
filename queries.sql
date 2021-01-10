select f1.filename, f1.path, f2.path
from files as f1
join files as f2 on f1.size = f2.size and f1.filename = f2.filename
where f1.path > f2.path




select f1.filename, f1.path, f2.path
from files as f1
join files as f2 on f1.size = f2.size and f1.filename = f2.filename
where f1.path < f2.path
order by f1.extension, f1.path