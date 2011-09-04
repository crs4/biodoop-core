SRC_DIR = ./proto
PY_OUT_DIR = ./details
PROTOCFLAGS = -I=$(SRC_DIR) --python_out=$(PY_OUT_DIR)

PROTOC = protoc
COMPILE.proto = $(PROTOC) $(PROTOCFLAGS)

SRC_FILES = $(wildcard $(SRC_DIR)/*.proto)
PY_OUT_FILES = $(subst proto,details,$(patsubst %.proto,%_pb2.py,$(SRC_FILES)))

python: $(PY_OUT_FILES)

$(PY_OUT_DIR)/%_pb2.py: $(SRC_DIR)/%.proto
	$(COMPILE.proto) $<

clean:
	rm -f $(PY_OUT_FILES)
