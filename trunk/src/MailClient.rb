=begin
Author: Davíð Halldór Lúðvíksson
Changed: 8.03.09
Licence: MIT
=end
require 'net/pop'

if ARGV.size <= 3
  puts 'Use: server port user pass'
  exit!
end

pop = Net::POP3.new(ARGV[0],ARGV[1])	#connects to POP3 Server
pop.start(ARGV[2],ARGV[3]) do |server|	#login with user and pass
  for msg in server.mails				#iterates through mails
    puts 'Mail messages:'
    text = msg.pop						#text gets mail in server.mails array
    puts text							#writes mail to console
    msg.delete							#delete post in inbox
  end
end
