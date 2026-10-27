.PHONY: run test stage4 stage5

run:
	./run.sh

stage4:
	./run.sh --script scripts/stage4_test.txt

stage5:
	./run.sh --script scripts/stage5_test.txt

test:
	python3 -m unittest discover -s tests
