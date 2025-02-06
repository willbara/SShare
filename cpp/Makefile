CXX = g++
CXXFLAGS = -fPIC -shared -I/usr/include/openssl
LIBS = -lcrypto

all: libencrypt.so

libencrypt.so: encryption.cpp
	$(CXX) $(CXXFLAGS) encryption.cpp -o libencrypt.so $(LIBS)

clean:
	rm -f libencrypt.so