CC = gcc
CFLAGS = -Wall -Wextra

TARGET = flame_cp
SCRIPT = errors.sh

.PHONY: all clean

all: $(TARGET)

$(TARGET): my_copy.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./errors.sh $(TARGET) $(ARGS)
