from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


#sin serialize devuelve algo como  <Object at 0x548138A5F>
#con el serialize devuelve  {"id": 1, "email": "pepe@pepe.pe", "profile": { "id": 1, "bio": "pepe el magnifico"} }
#relacion uno a uno entre users y profiles 


class Users(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    #relacion
    profile: Mapped["Profiles"] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "profile": self.profile.serialize()
            # do not serialize the password, its a security breach
        }

class Profiles(db.Model):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(String(250), nullable=True)
    #relacion
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="profile")

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
        }

#relacion uno a muchos entre teachers y courses
# cuando se reciba una lista, coleccion, array se tiene que serializar dentro de un loop (linea 56)

class Teachers(db.Model):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    #relacion
    courses: Mapped[list['Courses']] = relationship(back_populates='teacher')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "courses": [course.serialize() for course in self.courses]
        }
    
class Courses(db.Model):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    #relacion
    teacher: Mapped['Teachers'] = relationship(back_populates='courses')
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    enrollments: Mapped[list["Enrollments"]] = relationship(back_populates='course')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            #puedo acceder a la propiedad name del objeto teacher o serialize() SIN LOOP
            "teacher": self.teacher.name
        }
    
#relacion de muchos a muchos entre students, courses y enrollments

class Students(db.Model):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    #relacion con enrollments
    enrollments: Mapped[list['Enrollments']] = relationship(back_populates="student")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
           
        }
    
class Enrollments(db.Model):
    __tablename__ = 'enrollments'
 

    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'), primary_key=True)
    courses_id: Mapped[int] = mapped_column(ForeignKey('courses.id'), primary_key=True)
    #dato propio de la tabla Enrollments
    date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    student: Mapped['Students'] = relationship(back_populates="enrollments")
    course: Mapped['Courses'] = relationship(back_populates="enrollments")

    def serialize(self):
        return {
            "student_id": self.student_id,
            "course_id": self.courses_id,
            "date": self.date.isoFormat(),
        }