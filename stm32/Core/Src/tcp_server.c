/*
 * tcp_server.c
 *
 *  Created on: Jul 7, 2024
 *      Author: nkenn
 */


#include "lwip/opt.h"
#include "lwip/api.h"
#include "lwip/sys.h"
#include "lwip/tcp.h"
#include "string.h"
#include "message.h"
#include "command_manager.h"
#include "common.h"

#define SERVER_PORT 12345

static struct tcp_pcb *tcp_server_pcb;

static err_t tcp_server_accept(void *arg, struct tcp_pcb *newpcb, err_t err);
static err_t tcp_server_recv(void *arg, struct tcp_pcb *tpcb, struct pbuf *p, err_t err);
static void tcp_server_error(void *arg, err_t err);

void tcp_server_init(void) {
    tcp_server_pcb = tcp_new();
    if (tcp_server_pcb != NULL) {
        err_t err;
        err = tcp_bind(tcp_server_pcb, IP_ADDR_ANY, SERVER_PORT);
        if (err == ERR_OK) {
            tcp_server_pcb = tcp_listen(tcp_server_pcb);
            tcp_accept(tcp_server_pcb, tcp_server_accept);
        } else {
            // Handle error
        }
    } else {
        // Handle error
    }
}

static err_t tcp_server_accept(void *arg, struct tcp_pcb *newpcb, err_t err) {
    tcp_setprio(newpcb, TCP_PRIO_NORMAL);
    tcp_recv(newpcb, tcp_server_recv);
    tcp_err(newpcb, tcp_server_error);
    return ERR_OK;
}

static err_t tcp_server_recv(void *arg, struct tcp_pcb *tpcb, struct pbuf *p, err_t err) {
    if (p == NULL) {
        tcp_close(tpcb);
        tcp_recv(tpcb, NULL);
        return ERR_OK;
    } else {


        // Ensure the received data fits in the buffer
        if (p->tot_len <= COM_BUFFER_SIZE) {
            handle_request((uint8_t *)p->payload, tx_buffer);

            // Send the response back to the client
            if (tcp_write(tpcb, tx_buffer, COM_BUFFER_SIZE, TCP_WRITE_FLAG_COPY) != ERR_OK) {
                // Handle tcp_write error
            	char response[] = "TCP WRITE ERROR!";
            	tcp_write(tpcb, response, strlen(response), TCP_WRITE_FLAG_COPY);
            }
        } else {
            // Handle buffer overflow error
        	 const char *overflow_msg = "Buffer overflow error\n";
        	 tcp_write(tpcb, overflow_msg, strlen(overflow_msg), TCP_WRITE_FLAG_COPY);
        }

        // Free the pbuf after processing
        pbuf_free(p);
        return ERR_OK;
    }
}

static void tcp_server_error(void *arg, err_t err) {
    // Handle error
}
