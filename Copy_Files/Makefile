CC = gcc
CCFLAGS = -Wall -Wextra

TARGET = my_fm

.PHONY: all clean

all: $(TARGET)

$(TARGET): my_fm.c
	@$(CC) $(CFLAGS) -o $@ $^

clean:
	@rm -f $(TARGET)

run: $(TARGET)
	@./$(TARGET) $(ARGS)
