require 'net/pop'

pop = Net::POP3.new('192.168.1.34')
pop.start('dabbi', '1234') do |server|

  for msg in server.mails 
    puts 'Mail messages:'   
    text = msg.pop
    puts text
  end
end
