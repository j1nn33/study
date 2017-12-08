# ЗАМЕНА ipython notebook

cidr_mask='24'
   

mask_bits = int(cidr_mask.split('/')[-1])
print ('mask_bits', mask_bits)


bin_mask = '1'*mask_bits + '0'*(32-mask_bits)
print ('bin_mask', bin_mask)


dec_mask = [str(int(bin_mask[i:i+8], 2)) for i in range(0,25,8)]
dec_mask_str = '.'.join(dec_mask)
print ('dec_mask', dec_mask)

#result.append(ip_addr.format(ip_address, dec_mask_str))
#return result