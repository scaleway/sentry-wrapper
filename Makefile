shell:
	# Run database migrations
	docker-compose run --rm sentry upgrade --noinput
	# Create sentry user
	docker-compose run --rm sentry createuser \
		--email test \
		--password test \
		--superuser \
		--no-input \
			|| echo "=== OK, error messages are scary but they only mean the test user already exists"
	# Sentry configuration, so we don't have to set it manually from the web
	# interface
	docker-compose run --rm sentry config set system.admin-email test
	docker-compose run --rm sentry config set system.url-prefix "http://sentry:9000"
	docker-compose run --rm sentry config set auth.allow-registration false
	# Do not send reports to Sentry
	docker-compose run --rm sentry config set beacon.anonymous true
	docker-compose up -d
	# Run a shell to test sentry-wrapper
	docker run --rm -ti \
		-v `pwd`:/app -w /app \
		--network sentry-wrapper_default \
		python \
			sh -c 'pip install -ve python_project && pip install -ve . && bash'

clean:
	docker-compose kill
	docker-compose rm -f
