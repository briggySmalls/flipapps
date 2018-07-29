GRPC_BINDINGS = \
	flipapps/flipapps/protos/flipapps.proto \
	flipdot_assistant/flipdot_assistant/protos/flipapps.proto

TEST = $(call proto_source, $(firstword $(GRPC_BINDINGS)))

# Generate gRPC bindings for projects
grpc-bindings: $(GRPC_BINDINGS)

# Create a gRPC binding within the application
.SECONDEXPANSION:
%.proto: $$(call proto_source, $$@)
	@echo "Generating proto binding:" $@
	@mkdir -p $(dir $@)
	@echo > $(addsuffix /__init__.py, $(dir $@))
	@cp -r $(addprefix protos/, $(notdir $@)) $@
	@python -m grpc_tools.protoc \
		--proto_path=$(firstword $(subst /, ,$@)) \
		--python_out=$(firstword $(subst /, ,$@)) \
		--grpc_python_out=$(firstword $(subst /, ,$@)) $@

clean:
	rm -r $(GRPC_BINDINGS)

print-%:
	@echo $* = $($*)

define proto_source
	$(word 2, $(subst /protos/, protos/,$(1)))
endef
