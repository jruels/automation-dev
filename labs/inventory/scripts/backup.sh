#!/bin/sh

# Need to take a tag variable
# mediavars to test media
# webservervars to test webservers
# hostvar to test host var

case "$1" in
  mediavars)
    ansible-playbook -i inventory scripts/backup.yml --tags "mediavars"
    exit $?
    ;;
  webservervars)
    ansible-playbook -i inventory scripts/backup.yml --tags "webservervars"
    exit $?
    ;;
  hostvar)
    ansible-playbook -i inventory scripts/backup.yml --tags "hostvar"
    exit $?
    ;;
  *)
    ansible-playbook -i inventory scripts/backup.yml
    exit $?
esac
