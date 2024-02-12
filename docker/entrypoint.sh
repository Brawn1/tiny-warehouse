#!/usr/bin/env bash
set -e
umask 002

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
