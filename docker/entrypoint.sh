#!/usr/bin/env bash
set -e
umask 002

# set permissions on templates/media folder
chown -R django:django /web/templates && chmod -R 775 /web/templates


case "E$1" in
	Euwsgi)
		exec "$@"
		;;
  Emanage)
    su django -c "python /web/manage.py $@"
    ;;
	*)
		exec su django -c "$@"
		;;
esac

exec "$@"
