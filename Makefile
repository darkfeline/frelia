.PHONY: test
test:
	py.test --doctest-modules \
		--durations=5 \
		--cov=frelia --cov=tests --cov-report term-missing \
		frelia tests
