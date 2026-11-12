CC := cc
CPPFLAGS := -Iinclude -MMD -MP
CFLAGS := -std=c99 -Wall -Wextra -Werror -pedantic -O2
LDFLAGS :=
LDLIBS := -lm

SRC_DIR := src
BUILD_DIR := build
TARGET := tvid

SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $@

debug:
	$(MAKE) fclean
	$(MAKE) CFLAGS="-std=c99 -Wall -Wextra -Werror -g -O0 -fsanitize=address,undefined" \
	        LDFLAGS="-fsanitize=address,undefined"

clean:
	$(RM) -r $(BUILD_DIR)

fclean: clean
	$(RM) $(TARGET)

re: fclean
	$(MAKE) all

-include $(DEPS)

.PHONY: all debug clean fclean re
