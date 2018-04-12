GRPC_BINDINGS = \
	flipapps/flipapps/protos/flipapps.proto \
	flipdot_assistant/flipdot_assistant/protos/flipapps.proto

# Create a gRPC binding within the application
%.proto:
	mkdir $(dir $@)
	echo > $(addsuffix /__init__.py, $(dir $@))
	cp -r $(addprefix protos/, $(notdir $@)) $@
	python -m grpc_tools.protoc \
		--proto_path=$(firstword $(subst /, ,$@)) \
		--python_out=$(firstword $(subst /, ,$@)) \
		--grpc_python_out=$(firstword $(subst /, ,$@)) $@


# Generate gRPC bindings for projects
grpc-bindings: $(GRPC_BINDINGS)