require 'net/pop'

if ARGV.size <= 3
  puts 'Use: server port user pass'
  exit!
end

pop = Net::POP3.new(ARGV[0],ARGV[1])     #Connects to POP3 Server
pop.start(ARGV[2],ARGV[3]) do |server|   #Login with user and pass
  for msg in server.mails                #Iterates through mails
    puts 'Mail messages:'
    text = msg.pop                       #text gets first mail in server.mails array
    puts text
    msg.delete                           #delete post in inbox
  end
end
