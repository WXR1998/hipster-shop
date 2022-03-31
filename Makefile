.PHONY: run setup clean
run:
	skaffold run

setup: 
	@./setup.sh

clean:
	skaffold delete
	kubectl delete secrets lightstep-credentials
