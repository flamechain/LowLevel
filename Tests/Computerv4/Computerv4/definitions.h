#include <string>
#include <sstream>
#include <iomanip>

template <typename T>
inline std::string int_to_hex(T val, size_t width = sizeof(T) * 2) {
    std::stringstream ss;
    ss << std::setfill('0') << std::setw(width) << std::hex << (val | 0);
    return ss.str();
}
