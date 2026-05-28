//@version=5
indicator(" criptosefa Fibonacci Levels with Labels", overlay=true)
// Zaman aralığını al
current_resolution = timeframe.period

// En yüksek ve en düşük fiyatları hesapla (Son 150 mum)
highestHigh = request.security(syminfo.tickerid, current_resolution, ta.highest(high, 150))
lowestLow = request.security(syminfo.tickerid, current_resolution, ta.lowest(low, 150))

// Fibonacci seviyelerini hesapla
fib_0 = lowestLow
fib_100 = highestHigh
fib_neg_38_2 = lowestLow - (highestHigh - lowestLow) * 0.382
fib_neg_23_6 = lowestLow - (highestHigh - lowestLow) * 0.236
fib_23_6 = lowestLow + (highestHigh - lowestLow) * 0.236
fib_38_2 = lowestLow + (highestHigh - lowestLow) * 0.382
fib_50 = lowestLow + (highestHigh - lowestLow) * 0.5
fib_61_8 = lowestLow + (highestHigh - lowestLow) * 0.618
fib_78_6 = lowestLow + (highestHigh - lowestLow) * 0.786
fib_127_2 = highestHigh + (highestHigh - lowestLow) * 0.272
fib_141_4 = highestHigh + (highestHigh - lowestLow) * 0.414
fib_161_8 = highestHigh + (highestHigh - lowestLow) * 0.618

// Çizgilerin uzunluğunu ayarla
line_length = 50
start = bar_index
end = start + line_length

// Eski çizgileri yönetmek için bir liste kullan
var line[] fib_lines = array.new_line(0)

// Eski çizgileri sil
if array.size(fib_lines) > 0
    for i = 0 to array.size(fib_lines) - 1
        line.delete(array.get(fib_lines, i))
    array.clear(fib_lines)

// Fibonacci çizgilerini çiz ve listeye ekle
array.push(fib_lines, line.new(start, fib_0, end, fib_0, color=color.green, width=1))  // Dip (Yeşil)
array.push(fib_lines, line.new(start, fib_100, end, fib_100, color=color.red, width=1))  // Tepe (Kırmızı)
array.push(fib_lines, line.new(start, fib_neg_38_2, end, fib_neg_38_2, color=color.new(color.red, 50), width=1))  // Negatif Seviye
array.push(fib_lines, line.new(start, fib_neg_23_6, end, fib_neg_23_6, color=color.new(color.red, 50), width=1))  // Negatif Seviye
array.push(fib_lines, line.new(start, fib_23_6, end, fib_23_6, color=color.orange, width=1))  // Turuncu
array.push(fib_lines, line.new(start, fib_38_2, end, fib_38_2, color=color.orange, width=1))  // Turuncu
array.push(fib_lines, line.new(start, fib_50, end, fib_50, color=color.orange, width=1))  // Turuncu
array.push(fib_lines, line.new(start, fib_61_8, end, fib_61_8, color=color.orange, width=1))  // Turuncu
array.push(fib_lines, line.new(start, fib_78_6, end, fib_78_6, color=color.orange, width=1))  // Turuncu
array.push(fib_lines, line.new(start, fib_127_2, end, fib_127_2, color=#42040480, width=1))  // Negatif Seviye
array.push(fib_lines, line.new(start, fib_127_2, end, fib_127_2, color=#ce1d1d80, width=1))  // Negatif Seviye    
array.push(fib_lines, line.new(start, fib_141_4, end, fib_141_4, color=color.new(color.red, 50), width=1))  // Negatif Seviye
array.push(fib_lines, line.new(start, fib_161_8, end, fib_161_8, color=color.new(color.red, 50), width=1))  // Negatif Seviye



// Eski etiketleri yönetmek için bir liste kullan
var label[] fib_labels = array.new_label(0)

// Eski etiketleri sil
if array.size(fib_labels) > 0
    for i = 0 to array.size(fib_labels) - 1
        label.delete(array.get(fib_labels, i))
    array.clear(fib_labels)

// PHL ve PHH etiketlerini ekle
array.push(fib_labels, label.new(x=bar_index, y=fib_0, text="PHL", style=label.style_label_up, color=color.green, textcolor=color.white, size=size.small))
array.push(fib_labels, label.new(x=bar_index, y=fib_100, text="PHH", style=label.style_label_down, color=color.red, textcolor=color.white, size=size.small))

