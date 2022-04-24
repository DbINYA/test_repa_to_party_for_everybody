from data import db_session


def add_all_info(my_db, **kwargs):
	db_sess = db_session.create_session()
	for key in kwargs:
		setattr(my_db, key, kwargs[key])
	db_sess.add(my_db)
	db_sess.commit()


def work_with_date_users(list_of_ex):
	slovar = {}
	for i in list_of_ex:
		slovar[i.id] = [i.surname, i.name, i.patronymic, i.ava_photo, i.email]
	return slovar